package system


import "context"


// SystemInfo represents aggregated system-level metadata.
type SystemInfo struct {
OSName string `json:"os_name"`
OSPRETTY string `json:"os_pretty"`
Distro string `json:"distro,omitempty"`
Arch string `json:"arch"`
CPUCores int `json:"cpu_cores"`
TotalMemMB int `json:"total_mem_mb"`
Container bool `json:"containerized"`
WSL bool `json:"wsl"`
PathEntries []string `json:"path_entries"`
Meta map[string]interface{} `json:"meta,omitempty"`
}


// DetectSystem collects all system metadata in parallel.
func DetectSystem(ctx context.Context) SystemInfo {
info := SystemInfo{}


info.OSName, info.OSPRETTY = DetectOS()
info.Distro = DetectDistro()
info.Arch = DetectArch()
info.CPUCores = DetectCPU()
info.TotalMemMB = DetectMemory()
info.Container = DetectContainer()
info.WSL = DetectWSL()
info.PathEntries = DetectPathEntries()


return info
}
