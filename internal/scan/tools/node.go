package tools

import "context"

type NodeDetector struct{}


func (NodeDetector) Name() string { return "node" }

func (NodeDetector) Detect(ctx context.Context, root string) DetectorResult {
// node sometimes supports -v or --version; try both in order
return detectBinary(ctx, "node", []string{"node", "nodejs"}, []string{"--version"})
}
