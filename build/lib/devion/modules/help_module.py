from devion.interfaces.module_interface import DevionModuleInterface
from typing import Dict, Any

class HelpModule(DevionModuleInterface):
    """
    Provides a comprehensive list of all available Devion commands and their descriptions.
    This module adheres to the DevionModuleInterface.
    """

    def __init__(self, args: dict):
        """
        Initializes the Help module.
        It stores the arguments received from the CLI, although it typically requires none.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments. For the help command, this method ensures 
        it can always proceed without requiring specific flags or values.
        """
        # Help command requires no validation; simply return an empty dict for cleaned args.
        return {} 

    def execute(self) -> Dict[str, Any]:
        """
        Retrieves the list of commands and their descriptions.
        
        Returns:
            Dict: The data payload containing the 'commands' map and a message.
        """
        commands = {
            "init": "Initialize a new Devion project.",
            "status": "Check the installation status of all required tools.",
            "scan": "Scan the environment for configuration issues.",
            "analyze": "Analyze detected configuration and dependency issues.",
            "fix": "Automatically fix common issues.",
            "config": "Manage project configuration.",
            "use": "Switch between Devion modes or templates.",
            "deploy": "Deploy your project.",
            "help": "Show available commands and usage."
        }
        
        # We return the data payload, allowing the cli_bridge to wrap it in the 
        # final success/error envelope.
        return {
            "commands": commands,
            # Including a message here allows the bridge to use a custom message 
            # instead of a generic "success" one.
            "message": "📘 Devion command reference loaded successfully."
        }
