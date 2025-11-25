package tools

import "context"

type ApacheDetector struct{}

func (ApacheDetector) Name() string { return "apache" }

func (ApacheDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "apache", []string{"httpd", "apache2"}, []string{"-v"})
}
