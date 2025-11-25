package tools

import "context"

type NpmDetector struct{}


func (NpmDetector) Name() string { return "npm" }

func (NpmDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "npm", []string{"npm"}, []string{"--version"})
}
