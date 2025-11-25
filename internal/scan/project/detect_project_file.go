package project

import (
	"encoding/json"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// ProjectFilesInfo summarizes presence and basic metadata of key project files.
type ProjectFilesInfo struct {
	Root           string            `json:"root"`
	Files          map[string]bool   `json:"files"`
	DetectedAt     time.Time         `json:"detected_at"`
	DependencyMaps map[string]string `json:"dependency_files_content,omitempty"`
}

// KeyFiles is the list of files we check for in repository root.
var KeyFiles = []string{
	"package.json",
	"pyproject.toml",
	"requirements.txt",
	"Pipfile",
	"go.mod",
	"Cargo.toml",
	"Dockerfile",
	"docker-compose.yml",
	"docker-compose.yaml",
	"Makefile",
	".devion/config.json",
	".venv",
}

// DetectProjectFiles walks the repo root and detects existence of common files.
// It returns a ProjectFilesInfo with a boolean map and, for some dependency files,
// a small snippet of their content to help downstream detectors.
func DetectProjectFiles(root string) (ProjectFilesInfo, error) {
	info := ProjectFilesInfo{
		Root:           root,
		Files:          make(map[string]bool),
		DetectedAt:     time.Now().UTC(),
		DependencyMaps: make(map[string]string),
	}

	// normalize root
	root = filepath.Clean(root)

	// quick check in root for listed files
	for _, f := range KeyFiles {
		p := filepath.Join(root, f)
		if stat, err := os.Stat(p); err == nil {
			// mark existence; for dirs like .venv mark true
			if stat.IsDir() {
				info.Files[f] = true
			} else {
				info.Files[f] = true
				// read small content for certain dependency files
				if f == "package.json" || f == "go.mod" || f == "pyproject.toml" || f == "requirements.txt" {
					if b, err := os.ReadFile(p); err == nil {
						// store only first 16KB to avoid big payloads
						sz := len(b)
						if sz > 16*1024 {
							info.DependencyMaps[f] = string(b[:16*1024])
						} else {
							info.DependencyMaps[f] = string(b)
						}
					}
				}
			}
		} else {
			info.Files[f] = false
		}
	}

	// walk limited depth (top-level) to detect workspace/monorepo indicators
	_ = filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return nil
		}
		// skip nested dirs deeply
		rel, _ := filepath.Rel(root, path)
		if rel == "." {
			return nil
		}
		parts := strings.Split(rel, string(os.PathSeparator))
		if len(parts) > 2 {
			return fs.SkipDir
		}
		// detect package.json in subpackages (monorepo)
		if !d.IsDir() && strings.EqualFold(d.Name(), "package.json") {
			info.Files[filepath.ToSlash(rel)] = true
		}
		return nil
	})

	return info, nil
}

// Helper: parsePackageJSON tries to decode package.json into a map handy for other detectors.
func ParsePackageJSON(root string) (map[string]interface{}, error) {
	p := filepath.Join(filepath.Clean(root), "package.json")
	b, err := os.ReadFile(p)
	if err != nil {
		return nil, err
	}
	var m map[string]interface{}
	if err := json.Unmarshal(b, &m); err != nil {
		return nil, err
	}
	return m, nil
}

