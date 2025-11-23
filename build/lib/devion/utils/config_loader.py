import os
import json
from typing import Dict, Any

# Define constants for configuration paths
HOME_DIR = os.path.expanduser("~")
DEVION_DIR = os.path.join(HOME_DIR, ".devion")
CONFIG_FILE = os.path.join(DEVION_DIR, "config.json")

class ConfigLoader:
    """
    Utility class for handling Devion configuration files.
    Centralizes all logic related to reading/writing the config.json.
    """

    @staticmethod
    def get_config_path() -> str:
        """Returns the absolute path to the config file."""
        return CONFIG_FILE

    @staticmethod
    def ensure_config_dir() -> str:
        """
        Ensures the .devion directory exists.
        """
        os.makedirs(DEVION_DIR, exist_ok=True)
        return DEVION_DIR

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """
        Loads the configuration from disk.

        Returns:
            Dict[str, Any]: The configuration dictionary.
        
        Raises:
            FileNotFoundError: If the config file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError(f"Config file not found at {CONFIG_FILE}")

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_config(data: Dict[str, Any]) -> None:
        """
        Saves a dictionary to the configuration file.
        
        Args:
            data (Dict[str, Any]): The configuration data to save.
        """
        ConfigLoader.ensure_config_dir()
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
