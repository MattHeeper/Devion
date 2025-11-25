package tools

import "context"

type SbtDetector struct{}


func (SbtDetector) Name() string { return "sbt" }

func (SbtDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "sbt", []string{"sbt"}, []string{"--version"})
}
