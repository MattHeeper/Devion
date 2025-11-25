package tools

import "context"

type AzCliDetector struct{}

func (AzCliDetector) Name() string { return "azcli" }

func (AzCliDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "azcli", []string{"az"}, []string{"--version"})
}
