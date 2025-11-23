import os
import json
from typing import Dict, Any, Union

from devion.interfaces.module_interface import DevionModuleInterface

class ConfigModule(DevionModuleInterface):
    """
    Module responsible for managing the global configuration file (~/.devion/config.json).
    It supports reading the current config and updating specific settings.
    """

    def __init__(self, args: dict):
        """
        Initializes the Config module and sets the configuration path.
        """
        super().__init__(args)
        self.config_path = os.path.join(os.path.expanduser("~"), ".devion", "config.json")
        self.config: Dict[str, Any] = {}
        self.action: str = "read" # 'read' or 'update'

    def _load_config(self) -> bool:
        """
        Loads the configuration file into self.config.
        
        Returns:
            bool: True if the file was loaded successfully, False otherwise.
        """
        if not os.path.exists(self.config_path):
            return False
            
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            return True
        except json.JSONDecodeError:
            raise IOError(f"Configuration file is corrupted: {self.config_path}")

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments and determines the intended action ('read' or 'update').
        
        Args are expected to be passed as a dictionary from the Node CLI.
        Example CLI call: devion config --key language --value en
        Received args: {'key': 'language', 'value': 'en'}
        
        Returns:
            Dict: Validated arguments ready for execution.
        """
        validated_args: Dict[str, Any] = {}

        if not self.args:
            self.action = "read"
            return validated_args

        # Check for update operation arguments
        key = self.args.get('key')
        value = self.args.get('value')
        
        if key and value is not None:
            self.action = "update"
            validated_args['key'] = key
            validated_args['value'] = value
        elif key or value is not None:
             raise ValueError("Update operation requires both 'key' and 'value'.")
        else:
            self.action = "read"
            
        return validated_args

    def execute(self) -> Dict[str, Any]:
        """
        Runs the core logic: loads config and either displays it or updates a setting.
        
        Returns:
            Dict: The data payload containing the config or update confirmation.
        """
        # 1. Load configuration (Must be done first for both actions)
        if not self._load_config():
            # If config file is missing, return error immediately
            return {
                "config_path": self.config_path,
                "message": "Config file not found. Please run 'devion init' first.",
                "errors": ["Configuration file missing."],
            }
        
        # 2. Handle 'Read' action (default)
        if self.action == "read":
            return {
                "config": self.config,
                "message": "📄 Current Devion configuration loaded successfully.",
            }

        # 3. Handle 'Update' action
        key = self.args.get('key')
        value = self.args.get('value')

        if key in self.config.get("settings", {}):
            
            # Type conversion based on setting type (e.g., "true" -> True)
            if isinstance(self.config["settings"][key], bool):
                 new_value: Union[str, bool] = value.lower() == "true"
            else:
                 new_value = value
            
            self.config["settings"][key] = new_value

            # Write updated config back to file
            try:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(self.config, f, indent=2)
            except Exception as e:
                 raise IOError(f"Failed to save configuration: {e}")

            return {
                "config": self.config,
                "message": f"✅ Setting '{key}' updated successfully.",
            }
        else:
            # Unknown key error
            raise ValueError(f"Unknown config key: {key}. Available keys are: {list(self.config.get('settings', {}).keys())}")
