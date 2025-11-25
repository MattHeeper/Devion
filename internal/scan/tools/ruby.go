package tools

import "context"

type RubyDetector struct{}


func (RubyDetector) Name() string { return "ruby" }

func (RubyDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "ruby", []string{"ruby"}, []string{"--version"})
}
