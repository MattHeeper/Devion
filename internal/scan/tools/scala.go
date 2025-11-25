package tools

import "context"

type ScalaDetector struct{}


func (ScalaDetector) Name() string { return "scala" }

func (ScalaDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "scala", []string{"scala"}, []string{"-version"})
}
