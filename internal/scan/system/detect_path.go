package system


import (
"os"
"strings"
)


// DetectPathEntries returns PATH entries split by ":".
func DetectPathEntries() []string {
p := os.Getenv("PATH")
if p == "" {
return []string{}
}
return strings.Split(p, ":")
}
