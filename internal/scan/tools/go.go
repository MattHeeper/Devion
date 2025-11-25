package tools

import "context"

type GoDetector struct{}


func (GoDetector) Name() string { return "go" }

func (GoDetector) Detect(ctx context.Context, root string) DetectorResult {
// `go version` prints to stdout/stderr depending on platform
return detectBinary(ctx, "go", []string{"go"}, []string{"version"})
}
