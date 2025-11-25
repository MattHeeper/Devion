package tools

import "context"

type MysqlDetector struct{}

func (MysqlDetector) Name() string { return "mysql" }

func (MysqlDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "mysql", []string{"mysql"}, []string{"--version"})
}
