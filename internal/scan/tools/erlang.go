package tools

import "context"

type ErlangDetector struct{}


func (ErlangDetector) Name() string { return "erlang" }

func (ErlangDetector) Detect(ctx context.Context, root string) DetectorResult {
// erl prints -version differently; attempt erl -version
return detectBinary(ctx, "erlang", []string{"erl"}, []string{"-version"})
}
