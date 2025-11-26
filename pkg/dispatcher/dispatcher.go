package dispatcher

import (
	"fmt"
	"github.com/MattHeeper/Devion/pkg/scan"
	"github.com/spf13/cobra"
)

// Dispatch handles dispatching commands to the correct modules
func Dispatch(command string, payload map[string]interface{}) (map[string]interface{}, error) {
	switch command {
	case "scan":
		return scan.HandleScan(payload)
	default:
		return nil, fmt.Errorf("unknown command: %s", command)
	}
}

