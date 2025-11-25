package tools

import "context"

type PerlDetector struct{}


func (PerlDetector) Name() string { return "perl" }

func (PerlDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "perl", []string{"perl"}, []string{"--version"})
}
