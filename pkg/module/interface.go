package module

// Module defines the contract for all Devion backend modules.
// Each module handles a specific command such as status, scan, analyze, etc.
// Implementations must be deterministic, testable, and safe for single-call usage.
type Module interface {
    // Name returns the command name this module handles.
    Name() string

    // Validate normalizes and validates incoming arguments.
    // It must return an error if input is malformed.
    Validate(args map[string]interface{}) error

    // Execute performs the module's logic.
    // It returns a serializable result map and an optional error.
    Execute(args map[string]interface{}) (map[string]interface{}, error)
}

