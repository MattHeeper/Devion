package scan

import (
	"context"
	"time"
)

// DetectorResult is the canonical result returned by any detector.
// Fields are intentionally generic and serializable to JSON.
type DetectorResult struct {
	Name       string                 `json:"name"`
	Present    bool                   `json:"present"`
	Version    string                 `json:"version,omitempty"`
	Path       string                 `json:"path,omitempty"`
	Error      string                 `json:"error,omitempty"`
	DetectedBy string                 `json:"detected_by,omitempty"`
	Meta       map[string]interface{} `json:"meta,omitempty"`
	DurationMs int64                  `json:"duration_ms,omitempty"`
}

// Detector is the interface all tool/project/system detectors must implement.
// Detect should be safe to call concurrently. Respect the provided context for
// cancellation and timeouts and return promptly when ctx is Done().
type Detector interface {
	// Name returns a stable detector identifier, e.g. "git", "node", "project-files".
	Name() string

	// Detect performs the probe and returns a DetectorResult. The root parameter
	// is the repository root or working directory where project detectors should operate.
	Detect(ctx context.Context, root string) DetectorResult
}

// helper: small time-limited wrapper used by orchestrator. Detectors can use
// their own context handling, but the orchestrator will pass a context with timeout.
func withTimeout(parent context.Context, d time.Duration) (context.Context, context.CancelFunc) {
	if d <= 0 {
		return context.WithCancel(parent)
	}
	return context.WithTimeout(parent, d)
}

