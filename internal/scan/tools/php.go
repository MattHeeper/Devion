package tools

import "context"

type PHPDetector struct{}


func (PHPDetector) Name() string { return "php" }

func (PHPDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "php", []string{"php"}, []string{"--version"})
}
