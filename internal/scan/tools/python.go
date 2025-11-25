package tools

import "context"

type PythonDetector struct{}


func (PythonDetector) Name() string { return "python" }

func (PythonDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "python", []string{"python3", "python"}, []string{"--version"})
}
