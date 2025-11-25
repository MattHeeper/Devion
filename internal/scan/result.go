package scan

// ScanResult is the top-level structure returned by the scan orchestrator.
// It contains full system, tools, project, and recommendation information.
type ScanResult struct {
    Success         bool                   `json:"success"`
    ScannedAt       string                 `json:"scanned_at"`
    System          map[string]interface{} `json:"system"`
    Tools           map[string]ToolResult  `json:"tools"`
    Project         map[string]interface{} `json:"project"`
    Recommendations []Recommendation        `json:"recommendations,omitempty"`
}

// ToolResult represents the result for a single tool detector.
// Present = tool is found, Version & Path filled when available.
type ToolResult struct {
    Present    bool                   `json:"present"`
    Version    string                 `json:"version,omitempty"`
    Path       string                 `json:"path,omitempty"`
    Error      string                 `json:"error,omitempty"`
    DetectedBy string                 `json:"detected_by,omitempty"`
    Meta       map[string]interface{} `json:"meta,omitempty"`
    DurationMs int64                  `json:"duration_ms,omitempty"`
}

// Recommendation represents a single advisory entry generated from the scan.
type Recommendation struct {
    Tool        string `json:"tool"`
    Reason      string `json:"reason"`
    InstallCmd  string `json:"install_cmd,omitempty"`
    Level       string `json:"level"` // info, warn, error
    Fixable     bool   `json:"fixable"`
}

// scan.go
// Orchestrator for running all detectors concurrently with timeouts.
package scan

import (
    "context"
    "sync"
    "time"
)

type Orchestrator struct {
    detectors []Detector
    timeout   time.Duration
}

func NewOrchestrator(detectors []Detector, timeout time.Duration) *Orchestrator {
    return &Orchestrator{detectors: detectors, timeout: timeout}
}

func (o *Orchestrator) Run(ctx context.Context, root string) ScanResult {
    ctx, cancel := withTimeout(ctx, o.timeout)
    defer cancel()

    var wg sync.WaitGroup
    mu := sync.Mutex{}

    results := make(map[string]DetectorResult)

    for _, d := range o.detectors {
        det := d
        wg.Add(1)
        go func() {
            defer wg.Done()
            start := time.Now()
            res := det.Detect(ctx, root)
            res.DurationMs = time.Since(start).Milliseconds()

            mu.Lock()
            results[det.Name()] = res
            mu.Unlock()
        }()
    }

    wg.Wait()

    return ScanResult{
        Success:   true,
        ScannedAt: time.Now().UTC().Format(time.RFC3339),
        Tools:     results,
        System:    map[string]interface{}{},
        Project:   map[string]interface{}{},
    }
}

