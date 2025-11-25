package project

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
)

// ProjectType represents a classified project type.
type ProjectType struct {
	Type       string  `json:"type"`       // e.g., node:app, python:django
	Confidence float64 `json:"confidence"` // 0.0 - 1.0
	Details    string  `json:"details,omitempty"`
}

// DetectProjectType inspects root files and package.json/pyproject snippets to
// return best-effort project classification.
func DetectProjectType(root string) (ProjectType, error) {
	root = filepath.Clean(root)
	langs, _ := DetectLanguages(root)
	pt := ProjectType{Type: "unknown", Confidence: 0.0}
	if len(langs) == 0 {
		return pt, nil
	}

	// primary language
	primary := langs[0].Lang
	primaryScore := langs[0].Confidence

	switch primary {
	case "node":
		// look into package.json for frameworks (react, next, express)
		if m, err := ParsePackageJSON(root); err == nil {
			// check dependencies and scripts
			if deps, ok := m["dependencies"].(map[string]interface{}); ok {
				if _, hasNext := deps["next"]; hasNext {
					pt.Type = "node:next"
					pt.Confidence = primaryScore*0.9 + 0.1
					return pt, nil
				}
				if _, hasReact := deps["react"]; hasReact {
					pt.Type = "node:react"
					pt.Confidence = primaryScore*0.9 + 0.05
					return pt, nil
				}
				if _, hasExpress := deps["express"]; hasExpress {
					pt.Type = "node:express"
					pt.Confidence = primaryScore*0.85
					return pt, nil
				}
			}
			// fallback to generic node app
			pt.Type = "node:app"
			pt.Confidence = primaryScore
			return pt, nil
		}
		pt.Type = "node:app"
		pt.Confidence = primaryScore
		return pt, nil
	case "python":
		// check pyproject for frameworks
		p := filepath.Join(root, "pyproject.toml")
		if _, err := os.Stat(p); err == nil {
			b, _ := os.ReadFile(p)
			s := strings.ToLower(string(b))
			if strings.Contains(s, "django") {
				pt.Type = "python:django"
				pt.Confidence = primaryScore*0.9 + 0.1
				return pt, nil
			}
			if strings.Contains(s, "fastapi") {
				pt.Type = "python:fastapi"
				pt.Confidence = primaryScore*0.9 + 0.1
				return pt, nil
			}
		}
		pt.Type = "python:app"
		pt.Confidence = primaryScore
		return pt, nil
	case "go":
		if _, err := os.Stat(filepath.Join(root, "go.mod")); err == nil {
			pt.Type = "go:module"
			pt.Confidence = primaryScore
			return pt, nil
		}
		pt.Type = "go:unknown"
		pt.Confidence = primaryScore
		return pt, nil
	case "rust":
		if _, err := os.Stat(filepath.Join(root, "Cargo.toml")); err == nil {
			pt.Type = "rust:crate"
			pt.Confidence = primaryScore
			return pt, nil
		}
		pt.Type = "rust:unknown"
		pt.Confidence = primaryScore
		return pt, nil
	default:
		pt.Type = primary + ":unknown"
		pt.Confidence = primaryScore
		return pt, nil
	}
}

// Helper: SafeString returns a string prefix limited length
func SafeString(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}

// Optional: export a JSON helper
func ProjectTypeToJSON(pt ProjectType) (string, error) {
	b, err := json.Marshal(pt)
	if err != nil {
		return "", err
	}
	return string(b), nil
}

