package tools

import "context"

type RustcDetector struct{}


func (RustcDetector) Name() string { return "rustc" }

func (RustcDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "rustc", []string{"rustc"}, []string{"--version"})
}

