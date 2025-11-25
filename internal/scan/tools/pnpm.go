package tools

import "context"

type PnpmDetector struct{}


func (PnpmDetector) Name() string { return "pnpm" }

func (PnpmDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "pnpm", []string{"pnpm"}, []string{"--version"})
}
