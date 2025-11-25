package tools

import "context"

type AwsCliDetector struct{}

func (AwsCliDetector) Name() string { return "awscli" }

func (AwsCliDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "awscli", []string{"aws"}, []string{"--version"})
}
