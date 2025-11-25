package tools

import "context"

type OpensslDetector struct{}

func (OpensslDetector) Name() string { return "openssl" }

func (OpensslDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "openssl", []string{"openssl"}, []string{"version"})
}
