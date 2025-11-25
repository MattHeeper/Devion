package system


import (
"os/exec"
"strconv"
"strings"
)


// DetectMemory returns total RAM in MB.
func DetectMemory() int {
// Linux: use `grep MemTotal /proc/meminfo`
out, err := exec.Command("grep", "MemTotal", "/proc/meminfo").Output()
if err == nil {
fields := strings.Fields(string(out))
if len(fields) >= 2 {
kb, _ := strconv.Atoi(fields[1])
return kb / 1024
}
}
return 0
}
