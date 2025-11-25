package system


import (
"os"
"strings"
)


// DetectWSL detects Windows Subsystem for Linux.
func DetectWSL() bool {
data, err := os.ReadFile("/proc/version")
if err == nil && strings.Contains(strings.ToLower(string(data)), "wsl") {
return true
}
return false
}
