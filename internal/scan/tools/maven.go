package tools

import "context"

type MavenDetector struct{}


func (MavenDetector) Name() string { return "maven" }

func (MavenDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "mvn", []string{"mvn"}, []string{"--version"})
}
