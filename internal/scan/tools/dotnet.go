package tools

import "context"

type DotnetDetector struct{}


func (DotnetDetector) Name() string { return "dotnet" }

func (DotnetDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "dotnet", []string{"dotnet"}, []string{"--version"})
}
