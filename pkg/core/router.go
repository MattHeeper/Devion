package core

import (
    "errors"

    "github.com/MattHeeper/Devion/pkg/module"
    "github.com/MattHeeper/Devion/pkg/registry"
)

// Route locates and executes the appropriate module for a given command.
// It validates arguments, then runs the module's logic.
func Route(command string, args map[string]interface{}) (map[string]interface{}, error) {
    m := registry.Get(command)
    if m == nil {
        return nil, errors.New("unknown command: " + command)
    }

    if err := m.Validate(args); err != nil {
        return nil, err
    }

    return m.Execute(args)
}

