package tools

import "context"

type RedisDetector struct{}

func (RedisDetector) Name() string { return "redis" }

func (RedisDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "redis", []string{"redis-server"}, []string{"--version"})
}
