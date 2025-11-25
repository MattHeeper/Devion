package tools

import "context"

type GccDetector struct{}


func (GccDetector) Name() string { return "gcc" }

func (GccDetector) Detect(ctx context.Context, root string) DetectorResult {
// gcc -dumpversion is more stable across distros
return detectBinary(ctx, "gcc", []string{"gcc"}, []string{"-dumpversion"})
}
