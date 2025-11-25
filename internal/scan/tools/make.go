package tools

import "context"

type MakeDetector struct{}


func (MakeDetector) Name() string { return "make" }

func (MakeDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "make", []string{"make"}, []string{"--version"})
}
