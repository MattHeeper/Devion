package tools

import "context"

type JavacDetector struct{}


func (JavacDetector) Name() string { return "javac" }

func (JavacDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "javac", []string{"javac"}, []string{"-version"})
}
