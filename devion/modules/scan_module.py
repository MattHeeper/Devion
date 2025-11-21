import os
import shutil
import platform
import subprocess
from typing import Dict, Any, List, Optional

from devion.interfaces.module_interface import DevionModuleInterface

class ScanModule(DevionModuleInterface):
    """
    Module responsible for performing a deep scan of the host environment.
    It checks system specifications (OS, Arch) and the installation status 
    of critical development tools defined in the toolset.
    """

    def __init__(self, args: dict):
        """
        Initializes the Scan module.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments. The scan command currently operates without 
        mandatory arguments.
        
        Returns:
            Dict: Validated arguments.
        """
        return self.args

    def _check_tool(self, cmd: str, args: List[str]) -> Dict[str, Any]:
        """
        Helper method to check if a specific CLI tool is installed and retrieve its version.

        Args:
            cmd (str): The binary name (e.g., 'git').
            args (List[str]): Arguments to pass to get version (e.g., ['--version']).

        Returns:
            Dict[str, Any]: A dictionary containing installation status, version, and path.
        """
        tool_path = shutil.which(cmd)
        
        if not tool_path:
            return {
                "installed": False, 
                "version": None, 
                "path": None
            }

        try:
            # Execute the version command safely
            output = subprocess.check_output(
                [cmd] + args, 
                text=True, 
                stderr=subprocess.STDOUT
            ).strip()
            
            return {
                "installed": True, 
                "version": output, 
                "path": tool_path
            }
        except Exception as e:
            return {
                "installed": True, 
                "version": "unknown", 
                "path": tool_path, 
                "error": str(e)
            }

    def execute(self) -> Dict[str, Any]:
        """
        Runs the system scan logic.
        
        Returns:
            Dict: The data payload containing system info and tool statuses.
        """
        # Define the list of tools to check
        tools_to_scan = {
            "python": ["python3", "--version"],
            "node": ["node", "--version"],
            "npm": ["npm", "--version"],
            "git": ["git", "--version"],
            "docker": ["docker", "--version"],
        }

        scanned_tools = {}
        for tool_name, command_info in tools_to_scan.items():
            cmd = command_info[0]
            args = command_info[1:]
            scanned_tools[tool_name] = self._check_tool(cmd, args)

        # Check Devion configuration directory status
        devion_dir = os.path.expanduser("~/.devion")
        devion_exists = os.path.exists(devion_dir)

        result = {
            "system": {
                "os": platform.system(),
                "release": platform.release(),
                "arch": platform.machine(),
                "processor": platform.processor(),
            },
            "tools": scanned_tools,
            "devion_folder": {
                "exists": devion_exists,
                "path": devion_dir,
                "files": os.listdir(devion_dir) if devion_exists else [],
            },
        }

        return {
            "data": result,
            "message": "🔍 System scan completed successfully.",
        }
