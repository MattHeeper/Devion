package system


import (
"os"
"strings"
)


// DetectContainer checks if running inside Docker/Container.
func DetectContainer() bool {
// Docker: /proc/1/cgroup contains "docker" or "containerd"
data, err := os.ReadFile("/proc/1/cgroup")
if err == nil {
s := string(data)
if strings.Contains(s, "docker") || strings.Contains(s, "containerd") {
return true
}
}


// Also check /.dockerenv
if _, err := os.Stat("/.dockerenv"); err == nil {
return true
}
return false
}
