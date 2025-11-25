package tools

import "context"

type JavaDetector struct{}


func (JavaDetector) Name() string { return "java" }

func (JavaDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "java", []string{"java"}, []string{"-version"})
}
