package tools

import "context"

type GemDetector struct{}


func (GemDetector) Name() string { return "gem" }

func (GemDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "gem", []string{"gem"}, []string{"--version"})
}
