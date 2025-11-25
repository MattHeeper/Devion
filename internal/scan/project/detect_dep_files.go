package project

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"
)

// DependencySummary holds extracted dependency info from common files.
type DependencySummary struct {
	HasPackageJSON bool              `json:"has_package_json"`
	Engines        map[string]string `json:"engines,omitempty"`
	Scripts        []string          `json:"scripts,omitempty"`
	GoRequires     []string          `json:"go_requires,omitempty"`
	PythonReqs     []string          `json:"python_requirements,omitempty"`
}

// DetectDependencyFiles inspects common dependency files and extracts small summaries.
func DetectDependencyFiles(root string) (DependencySummary, error) {
	root = filepath.Clean(root)
	s := DependencySummary{Engines: make(map[string]string)}

	// package.json
	pj := filepath.Join(root, "package.json")
	if b, err := os.ReadFile(pj); err == nil {
		s.HasPackageJSON = true
		// quick naive parse for engines and scripts (string search, zero-deps)
		str := string(b)
		if idx := strings.Index(str, "\"engines\""); idx >= 0 {
			// attempt to capture engines block between braces
			sub := str[idx:]
			// crude: find first { and the matching }
			open := strings.Index(sub, "{")
			close := strings.Index(sub, "}")
			if open >= 0 && close > open {
				eng := sub[open+1 : close]
				// look for common engine keys
				if strings.Contains(eng, "node") {
					// extract approximate version
					parts := strings.Split(eng, ":")
					if len(parts) > 1 {
						s.Engines["node"] = strings.Trim(parts[1], " \" ,\n")
					}
				}
			}
		}
		// scripts
		if strings.Contains(str, "\"scripts\"") {
			// crude extraction: find occurrences of "run": "..."
			lines := strings.Split(str, "\n")
			for _, L := range lines {
				if strings.Contains(L, "\"scripts\"") {
					continue
				}
				if strings.Contains(L, "\"") && strings.Contains(L, ": \"") {
					// naive parse
					p := strings.SplitN(L, ": \"", 2)
					if len(p) == 2 {
						name := strings.Trim(p[0], " \" ,")
						if name != "" && name != "scripts" {
							s.Scripts = append(s.Scripts, name)
						}
					}
				}
			}
		}
	}

	// go.mod
	gm := filepath.Join(root, "go.mod")
	if b, err := os.ReadFile(gm); err == nil {
		lines := strings.Split(string(b), "\n")
		for _, l := range lines {
			l = strings.TrimSpace(l)
			if strings.HasPrefix(l, "require ") {
				parts := strings.Fields(l)
				if len(parts) >= 2 {
					s.GoRequires = append(s.GoRequires, parts[1])
				}
			}
		}
	}

	// requirements.txt - list each non-comment line
	rq := filepath.Join(root, "requirements.txt")
	if f, err := os.Open(rq); err == nil {
		defer f.Close()
		sc := bufio.NewScanner(f)
		for sc.Scan() {
			ln := strings.TrimSpace(sc.Text())
			if ln == "" || strings.HasPrefix(ln, "#") {
				continue
			}
			s.PythonReqs = append(s.PythonReqs, ln)
		}
	}

	return s, nil
}

