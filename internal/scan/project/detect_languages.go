package project

import (
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

// LanguageScore represents a detected language and a confidence score [0.0-1.0].
type LanguageScore struct {
	Lang       string  `json:"lang"`
	Confidence float64 `json:"confidence"`
}

// DetectLanguages scans top-level files and a limited set of extensions to produce
// a ranked list of detected languages with confidence scores.
func DetectLanguages(root string) ([]LanguageScore, error) {
	langCounts := map[string]int{}
	total := 0
	root = filepath.Clean(root)

	// quick checks for primary files
	checks := map[string]string{
		"package.json": "node",
		"go.mod":       "go",
		"pyproject.toml": "python",
		"requirements.txt": "python",
		"Cargo.toml":   "rust",
		"composer.json": "php",
	}
	for f, lang := range checks {
		if _, err := os.Stat(filepath.Join(root, f)); err == nil {
			langCounts[lang] += 10 // heavy weight
			total += 10
		}
	}

	// scan top 200 files by extension for heuristics
	count := 0
	_ = filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return nil
		}
		if d.IsDir() {
			// skip node_modules, .git, vendor
			n := d.Name()
			if n == "node_modules" || n == ".git" || n == "vendor" {
				return filepath.SkipDir
			}
			return nil
		}
		ext := strings.ToLower(filepath.Ext(d.Name()))
		switch ext {
		case ".js", ".jsx", ".ts", ".tsx":
			langCounts["node"]++
			total++
		case ".go":
			langCounts["go"]++
			total++
		case ".py":
			langCounts["python"]++
			total++
		case ".rs":
			langCounts["rust"]++
			total++
		case ".php":
			langCounts["php"]++
			total++
		case ".java":
			langCounts["java"]++
			total++
		case ".swift":
			langCounts["swift"]++
			total++
		}
		count++
		if count > 200 {
			return filepath.SkipDir
		}
		return nil
	})

	// normalize into LanguageScore slice
	res := []LanguageScore{}
	for k, v := range langCounts {
		score := 0.0
		if total > 0 {
			score = float64(v) / float64(total)
		}
		res = append(res, LanguageScore{Lang: k, Confidence: score})
	}

	// sort by confidence descending
	for i := 0; i < len(res); i++ {
		for j := i + 1; j < len(res); j++ {
			if res[j].Confidence > res[i].Confidence {
				res[i], res[j] = res[j], res[i]
			}
		}
	}

	return res, nil
}

