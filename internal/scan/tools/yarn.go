package tools

import "context"

type YarnDetector struct{}


func (YarnDetector) Name() string { return "yarn" }

func (YarnDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "yarn", []string{"yarn"}, []string{"--version"})
}
