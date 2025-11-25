package system


import (
"os"
"strings"
)


// DetectDistro extracts distro ID from /etc/os-release.
func DetectDistro() string {
data, err := os.ReadFile("/etc/os-release")
if err != nil {
return "unknown"
}
lines := strings.Split(string(data), "\n")
for _, l := range lines {
if strings.HasPrefix(l, "ID=") {
return strings.Trim(l[len("ID="):], "\"")
}
}
return "linux"
}


