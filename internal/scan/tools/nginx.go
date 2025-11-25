package tools

import "context"

type NginxDetector struct{}

func (NginxDetector) Name() string { return "nginx" }

func (NginxDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "nginx", []string{"nginx"}, []string{"-v"})
}
