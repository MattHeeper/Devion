package tools

import "context"

type LuaDetector struct{}


func (LuaDetector) Name() string { return "lua" }

func (LuaDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "lua", []string{"lua"}, []string{"-v"})
}
