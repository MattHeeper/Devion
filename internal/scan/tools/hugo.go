package tools

import "context"

type HugoDetector struct{}

func (HugoDetector) Name() string { return "hugo" }

func (HugoDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "hugo", []string{"hugo"}, []string{"version"})
}
