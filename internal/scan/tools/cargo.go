package tools

import "context"

type CargoDetector struct{}

func (CargoDetector) Name() string { return "cargo" }

func (CargoDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "cargo", []string{"cargo"}, []string{"--version"})
}
