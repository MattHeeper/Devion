package tools

import "context"

type KubectlDetector struct{}


func (KubectlDetector) Name() string { return "kubectl" }

func (KubectlDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "kubectl", []string{"kubectl"}, []string{"version", "--client"})
}
