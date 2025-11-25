package tools

import "context"

type DockerDetector struct{}


func (DockerDetector) Name() string { return "docker" }

func (DockerDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "docker", []string{"docker"}, []string{"--version"})
}
