package tools

import "context"

type ComposerDetector struct{}


func (ComposerDetector) Name() string { return "composer" }

func (ComposerDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "composer", []string{"composer"}, []string{"--version"})
}
