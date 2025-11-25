package tools

import "context"

type GcloudDetector struct{}

func (GcloudDetector) Name() string { return "gcloud" }

func (GcloudDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "gcloud", []string{"gcloud"}, []string{"--version"})
}
