import os
import json
from datetime import datetime
from typing import Dict, Any

from devion.interfaces.module_interface import DevionModuleInterface

class InitModule(DevionModuleInterface):
    """
    Module responsible for initializing the Devion environment by creating 
    the necessary configuration directory and default config file in the 
    user's home directory (~/.devion).
    """

    def __init__(self, args: dict):
        """
        Initializes the Init module.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments. The initialization process does not typically 
        require user-supplied arguments, focusing only on system paths.
        
        Returns:
            Dict: Empty dictionary as no user arguments are processed here.
        """
        # No specific arguments needed for initialization.
        return {} 

    def execute(self) -> Dict[str, Any]:
        """
        Runs the core initialization logic: creates directory and writes config.
        
        Returns:
            Dict: The data payload confirming the configuration path.
        """
        home_dir = os.path.expanduser("~")
        devion_dir = os.path.join(home_dir, ".devion")
        config_file = os.path.join(devion_dir, "config.json")

        # Create the .devion directory if it doesn't exist
        os.makedirs(devion_dir, exist_ok=True)

        default_config = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "settings": {
                "auto_update": True,
                "language": "en",
                "color_output": True
            }
        }

        # Write the default configuration file
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
                
            return {
                "config_path": config_file,
                "message": f"✅ Devion initialized successfully at {config_file}",
            }
        except Exception as e:
            # Raise an exception if writing fails (which the cli_bridge will catch)
            raise IOError(f"Failed to write configuration file to {config_file}: {e}")
