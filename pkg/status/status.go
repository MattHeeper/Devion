package status

import (
    "runtime"

    "github.com/MattHeeper/devion-go/pkg/module"
    "github.com/MattHeeper/devion-go/pkg/registry"
)

// ModuleStatus implements the status inspection command.
type ModuleStatus struct{}

// Name returns the command handled by this module.
func (ModuleStatus) Name() string { return "status" }

// Validate performs basic argument validation for the status command.
func (ModuleStatus) Validate(args map[string]interface{}) error {
    return nil // no arguments required
}

// Execute gathers extended system information.
func (ModuleStatus) Execute(args map[string]interface{}) (map[string]interface{}, error) {
    // Base system info
    var mem runtime.MemStats
    runtime.ReadMemStats(&mem)

    // System uptime (Unix-based)
    uptime := "unknown"
    if data, err := os.ReadFile("/proc/uptime"); err == nil {
        fields := strings.Fields(string(data))
        if len(fields) > 0 {
            uptime = fields[0]
        }
    }

    // Detect shell
    shell := os.Getenv("SHELL")

    // Detect Linux distro
    distro := "unknown"
    if data, err := os.ReadFile("/etc/os-release"); err == nil {
        lines := strings.Split(string(data), "
")
        for _, line := range lines {
            if strings.HasPrefix(line, "PRETTY_NAME=") {
                distro = strings.Trim(strings.SplitN(line, "=", 2)[1], "\"")
                break
            }
        }
    }

    // Base system info updated
    out := map[string]interface{}{
        "os":         runtime.GOOS,
        "arch":       runtime.GOARCH,
        "go_runtime": runtime.Version(),
        "memory_usage_bytes": mem.Alloc,
        "uptime_seconds":     uptime,
        "shell":              shell,
        "distro":             distro,
    }

    // ENV information
    home, _ := os.UserHomeDir()
    cwd, _ := os.Getwd()
    out["env"] = map[string]interface{}{
        "home": home,
        "cwd":  cwd,
    }

    // Config existence check
    configPath := filepath.Join(home, ".devion", "config.json")
    if _, err := os.Stat(configPath); err == nil {
        out["config_exists"] = true
    } else {
        out["config_exists"] = false
    }

    // Network reachability (simple TCP dial)
    reachable := false
    conn, err := net.DialTimeout("tcp", "8.8.8.8:53", time.Millisecond*500)
    if err == nil {
        reachable = true
        conn.Close()
    }
    out["network"] = map[string]interface{}{
        "reachable": reachable,
    }

    // Timezone
    loc := time.Now().Location()
    out["timezone"] = loc.String()

    return out, nil
}

// Automatic registration.
func init() {
    registry.Register(ModuleStatus{})
}

