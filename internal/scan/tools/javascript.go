package tools

import "context"

type JavascriptDetector struct{}

func (JavascriptDetector) Name() string { return "javascript" }

func (JavascriptDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "javascript", []string{"node", "nodejs"}, []string{"--version"})
}
