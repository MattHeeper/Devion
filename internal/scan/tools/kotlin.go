package tools

import "context"

type KotlinDetector struct{}


func (KotlinDetector) Name() string { return "kotlin" }

func (KotlinDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "kotlin", []string{"kotlinc"}, []string{"-version"})
}
