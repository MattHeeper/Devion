package tools

import "context"

type GradleDetector struct{}


func (GradleDetector) Name() string { return "gradle" }

func (GradleDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "gradle", []string{"gradle"}, []string{"--version"})
}
