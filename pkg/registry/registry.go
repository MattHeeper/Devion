package registry

import (
    "sync"

    "github.com/MattHeeper/Devion/pkg/module"
)

// Registry stores all module implementations mapped by their command name.
// This allows dynamic lookup similar to the previous Python COMMAND_MAP.
// The registry is concurrency-safe and read-optimized.
var (
    mu      sync.RWMutex
    modules = make(map[string]module.Module)
)

// Register adds a module to the registry. Each module must have a unique Name().
// Typically called from init() of each module package or from a central initializer.
func Register(m module.Module) {
    mu.Lock()
    modules[m.Name()] = m
    mu.Unlock()
}

// Get retrieves a module by its command name. Returns nil if not found.
func Get(name string) module.Module {
    mu.RLock()
    defer mu.RUnlock()
    return modules[name]
}

// List returns a slice of all registered module names.
// Useful for debugging, testing, or generating help output.
func List() []string {
    mu.RLock()
    defer mu.RUnlock()

    out := make([]string, 0, len(modules))
    for name := range modules {
        out = append(out, name)
    }
    return out
}
