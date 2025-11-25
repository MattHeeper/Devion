package tools

import "context"

type TerraformDetector struct{}

func (TerraformDetector) Name() string { return "terraform" }

func (TerraformDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "terraform", []string{"terraform"}, []string{"version"})
}
