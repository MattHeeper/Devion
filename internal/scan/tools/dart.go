package tools

import "context"

type DartDetector struct{}


func (DartDetector) Name() string { return "dart" }

func (DartDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "dart", []string{"dart"}, []string{"--version"})
}
