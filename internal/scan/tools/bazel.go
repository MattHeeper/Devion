package tools

import "context"

type BazelDetector struct{}

func (BazelDetector) Name() string { return "bazel" }

func (BazelDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "bazel", []string{"bazel"}, []string{"--version"})
}
