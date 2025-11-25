package tools

import "context"

type GitDetector struct{}


func (GitDetector) Name() string { return "git" }

func (GitDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "git", []string{"git"}, []string{"--version"})
