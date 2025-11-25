package tools

import "context"

type PostgresDetector struct{}

func (PostgresDetector) Name() string { return "postgres" }

func (PostgresDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "postgres", []string{"psql"}, []string{"--version"})
}
