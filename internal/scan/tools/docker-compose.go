package tools

import "context"

type DockerComposeDetector struct{}

func (DockerComposeDetector) Name() string { return "docker-compose" }

func (DockerComposeDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "docker-compose", []string{"docker-compose", "docker"}, []string{"compose", "version"})
}
