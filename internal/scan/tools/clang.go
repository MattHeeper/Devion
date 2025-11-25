package tools

import "context"

type ClangDetector struct{}


func (ClangDetector) Name() string { return "clang" }

func (ClangDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "clang", []string{"clang"}, []string{"--version"})
}
