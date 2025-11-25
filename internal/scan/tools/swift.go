package tools

import "context"

type SwiftDetector struct{}


func (SwiftDetector) Name() string { return "swift" }

func (SwiftDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "swift", []string{"swift"}, []string{"--version"})
}
