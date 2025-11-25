package tools

import "context"

type ElixirDetector struct{}


func (ElixirDetector) Name() string { return "elixir" }

func (ElixirDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "elixir", []string{"elixir"}, []string{"--version"})
}
