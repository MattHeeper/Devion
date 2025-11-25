package tools

import "context"

type AnsibleDetector struct{}

func (AnsibleDetector) Name() string { return "ansible" }

func (AnsibleDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "ansible", []string{"ansible"}, []string{"--version"})
}
