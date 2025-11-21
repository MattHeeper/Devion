import os
import json
import shutil
from datetime import datetime
import subprocess
from typing import Dict, Any, List

from devion.interfaces.module_interface import DevionModuleInterface

class FixModule(DevionModuleInterface):
    """
    Module responsible for checking and automatically fixing common environment 
    and configuration issues (e.g., creating missing config files, checking tool paths).
    """

    def __init__(self, args: dict):
        """
        Initializes the Fix module.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments. The fix command typically accepts no arguments 
        or very specialized ones (e.g., --force).
        
        Returns:
            Dict: Cleaned and validated arguments.
        """
        # Future logic for handling '--force' or other fix options would go here.
        return self.args 

    def _check_and_fix_environment(self, fixed_items: List[str], errors: List[str]):
        """
        Checks for and creates the required .devion directory and config file.
        """
        home_dir = os.path.expanduser("~")
        devion_dir = os.path.join(home_dir, ".devion")
        config_file = os.path.join(devion_dir, "config.json")

        if not os.path.exists(devion_dir):
            try:
                os.makedirs(devion_dir, exist_ok=True)
                fixed_items.append("Created missing .devion directory")
            except OSError as e:
                errors.append(f"Failed to create .devion directory: {e}")

        if not os.path.exists(config_file):
            default_config = {
                "created_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "settings": {
                    "auto_update": True,
                    "language": "en",
                    "color_output": True
                }
            }
            try:
                with open(config_file, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2)
                fixed_items.append("Recreated missing config.json")
            except IOError as e:
                errors.append(f"Failed to write config.json: {e}")
                
        return config_file

    def _check_and_report_tools(self, fixed_items: List[str], errors: List[str]) -> List[str]:
        """
        Checks for the presence of critical system tools.
        """
        tools = {
            "python": "python3 --version",
            "node": "node --version",
            "npm": "npm --version",
            "git": "git --version"
        }

        missing_tools = []
        for tool, cmd in tools.items():
            try:
                # Use shell=False for better security if possible, but keeping shell=True 
                # to respect the original code's execution style for now.
                subprocess.run(
                    cmd, 
                    shell=True, 
                    check=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing_tools.append(tool)

        if missing_tools:
            errors.append(f"Missing tools detected: {', '.join(missing_tools)}")
        else:
            fixed_items.append("All required tools confirmed installed")
            
        return missing_tools

    def execute(self) -> Dict[str, Any]:
        """
        Runs the core fix logic by repairing configuration and checking tools.
        
        Returns:
            Dict: The data payload containing the fix results and status.
        """
        fixed_items: List[str] = []
        errors: List[str] = []

        # 1. Check and fix the local environment files
        config_file = self._check_and_fix_environment(fixed_items, errors)
        
        # 2. Check system tool dependencies
        missing_tools = self._check_and_report_tools(fixed_items, errors)
        
        # Determine the final message based on the error count
        message = (
            "⚙️ System fix completed successfully." 
            if not errors 
            else "⚠️ Fix completed with some issues."
        )

        # Return the data payload
        return {
            "fixed_items": fixed_items,
            "missing_tools": missing_tools,
            "config_path": config_file,
            "message": message,
            # Include errors in the payload for the bridge to determine success=False
            "errors": errors 
        }
