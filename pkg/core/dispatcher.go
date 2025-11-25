package core

import (
    "github.com/MattHeeper/Devion/pkg/core"
)

// Dispatch is the top-level entry used by the CLI layer.
// It forwards the incoming command and arguments to the router.
// The CLI should only call Dispatch, never the router directly.
func Dispatch(command string, args map[string]interface{}) (map[string]interface{}, error) {
    return core.Route(command, args)
}

