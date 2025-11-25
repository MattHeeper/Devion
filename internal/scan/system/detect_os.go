package system


import (
"os"
"runtime"
"strings"
)


// DetectOS returns OS name and pretty name.
func DetectOS() (string, string) {
osname := runtime.GOOS
pretty := ""


// Linux: read /etc/os-release
if osname == "linux" {
data, err := os.ReadFile("/etc/os-release")
if err == nil {
lines := strings.Split(string(data), "\n")
for _, l := range lines {
if strings.HasPrefix(l, "PRETTY_NAME=") {
pretty = strings.Trim(l[len("PRETTY_NAME="):], "\"")
}
}
}
}


if pretty == "" {
pretty = osname
}


return osname, pretty
}


// DetectArch returns system architecture.
func DetectArch() string {
return runtime.GOARCH
}
