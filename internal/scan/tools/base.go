package tools

import (
    "context"
    "os/exec"
    "strings"
    "time"
)

type DetectorResult struct {
    Name       string
    Present    bool
    Version    string
    Path       string
    Error      string
    DetectedBy string
    DurationMs int64
}

// Shared binary-detection helper
func detectBinary(ctx context.Context, id string, candidates []string, args []string) DetectorResult {
    start := time.Now()
    for _, cand := range candidates {
        path, err := exec.LookPath(cand)
        if err != nil {
            continue
        }

        runArgs := args
        if len(runArgs) == 0 {
            runArgs = []string{"--version"}
        }

        out, err := exec.CommandContext(ctx, path, runArgs...).CombinedOutput()
        res := DetectorResult{
            Name:       id,
            Present:    true,
            Path:       path,
            DetectedBy: cand + " " + strings.Join(runArgs, " "),
            DurationMs: time.Since(start).Milliseconds(),
        }
        if err != nil {
            res.Error = strings.TrimSpace(err.Error())
            if len(out) > 0 {
                res.Version = strings.TrimSpace(string(out))
            }
            return res
        }
        res.Version = strings.TrimSpace(string(out))
        return res
    }
    return DetectorResult{
        Name:       id,
        Present:    false,
        Error:      "not found",
        DurationMs: time.Since(start).Milliseconds(),
    }
}

