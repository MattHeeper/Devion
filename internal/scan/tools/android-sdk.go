package tools

import "context"

type AndroidSDKDetector struct{}

func (AndroidSDKDetector) Name() string { return "android-sdk" }

func (AndroidSDKDetector) Detect(ctx context.Context, root string) DetectorResult {
return detectBinary(ctx, "android-sdk", []string{"sdkmanager"}, []string{"--version"})
}
