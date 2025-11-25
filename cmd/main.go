package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/MattHeeper/devion-go/pkg/dispatcher"
)

var jsonFlag bool

func main() {
	root := &cobra.Command{
		Use:   "devion",
		Short: "Devion CLI — Development environment manager",
		Long:  "Devion is a modular CLI for inspecting and fixing developer environment issues.",
	}

	root.PersistentFlags().BoolVar(&jsonFlag, "json", false, "output machine-readable JSON")

	commands := []string{"status", "scan", "analyze", "fix", "deploy", "config", "init", "use", "help"}

	for _, name := range commands {
		n := name
		cmd := &cobra.Command{
			Use:   n,
			Short: fmt.Sprintf("Run %s command", n),
			RunE: func(cmd *cobra.Command, args []string) error {
				payload := map[string]interface{}{}

				res, err := dispatcher.Dispatch(n, payload)
				if err != nil {
					return err
				}

				if jsonFlag {
					enc := json.NewEncoder(os.Stdout)
					enc.SetIndent("", "  ")
					return enc.Encode(res)
				}

				if msg, ok := res["message"]; ok {
					fmt.Println(msg)
				}
				pretty, _ := json.MarshalIndent(res, "", "  ")
				fmt.Println(string(pretty))
				return nil
			},
		}
		root.AddCommand(cmd)
	}

	if err := root.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}


