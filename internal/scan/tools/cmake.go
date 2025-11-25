package tools

import "context"

type CMakeDetector struct{}

func (CMakeDetector) Name() string { return "cmake" }

func (CMakeDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "cmake", []string{"cmake"}, []string{"--version"})
}
