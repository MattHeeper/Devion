import shutil
import subprocess
from typing import Dict, Any, List, Optional

from devion.interfaces.module_interface import DevionModuleInterface

class StatusModule(DevionModuleInterface):
    """
    Module responsible for checking the presence and versions of core development tools.
    It provides a summary of installed vs. missing tools.
    """

    def __init__(self, args: dict):
        """
        Initializes the Status module.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments. 
        The status command accepts optional flags like 'verbose' (handled in execute).
        
        Returns:
            Dict: Validated arguments.
        """
        return self.args

    def _check_tool(self, cmd: str, args: List[str]) -> Dict[str, Any]:
        """
        Internal helper to check if a tool exists and get its version.
        
        Args:
            cmd (str): The binary name (e.g., 'python3').
            args (List[str]): Arguments to fetch version.
            
        Returns:
            Dict: Status object containing 'installed', 'version', and 'path'.
        """
        tool_path = shutil.which(cmd)
        
        if not tool_path:
            return {"installed": False, "version": None, "path": None}

        try:
            # Run command to get version string
            output = subprocess.check_output(
                [cmd] + args, 
                text=True, 
                stderr=subprocess.STDOUT
            ).strip()
            
            # Basic cleanup of version string (taking the first line)
            version_clean = output.split('\n')[0]
            
            return {
                "installed": True, 
                "version": version_clean, 
                "path": tool_path
            }
        except Exception:
            return {
                "installed": True, 
                "version": "unknown", 
                "path": tool_path
            }

    def execute(self) -> Dict[str, Any]:
        """
        Runs the tool checks and prepares a summarized report.
        
        Returns:
            Dict: The data payload containing tool details and a summary count.
        """
        # Define tools to check
        target_tools = {
            "python": ["python3", "--version"],
            "node": ["node", "--version"],
            "npm": ["npm", "--version"],
            "git": ["git", "--version"],
            "docker": ["docker", "--version"],
        }

        tools_status = {}
        installed_count = 0
        formatted_output = {}

        # 1. Check each tool
        for name, cmd_info in target_tools.items():
            result = self._check_tool(cmd_info[0], cmd_info[1:])
            tools_status[name] = result
            
            if result["installed"]:
                installed_count += 1
                formatted_output[name] = f"✅ {result['version']}"
            else:
                formatted_output[name] = "❌ Not installed"

        total_count = len(target_tools)
        missing_count = total_count - installed_count

        # 2. Construct the final data payload
        return {
            "tools": tools_status,
            "formatted": formatted_output,  # Included for UI compatibility
            "summary": {
                "installed": installed_count,
                "total": total_count,
                "missing": missing_count,
            },
            "message": f"{installed_count}/{total_count} tools installed."
        }
