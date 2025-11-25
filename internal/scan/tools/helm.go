package tools

import "context"

type HelmDetector struct{}

func (HelmDetector) Name() string { return "helm" }

func (HelmDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "helm", []string{"helm"}, []string{"version"})
}
