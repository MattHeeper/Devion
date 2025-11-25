package tools

import "context"

type PipDetector struct{}


func (PipDetector) Name() string { return "pip" }

func (PipDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "pip", []string{"pip3", "pip"}, []string{"--version"})
}
