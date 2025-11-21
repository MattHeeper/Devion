import shutil
import subprocess
from typing import Dict, Any, Optional

def check_tool_availability(cmd: str, version_flag: str = "--version") -> Dict[str, Any]:
    """
    Checks if a specific command-line tool is available in the system path
    and attempts to retrieve its version.

    This generic function replaces the need for separate functions per tool.

    Args:
        cmd (str): The binary name of the tool (e.g., 'git', 'python3').
        version_flag (str): The flag used to request the version (default: '--version').

    Returns:
        Dict[str, Any]: A dictionary containing:
            - installed (bool): True if found.
            - version (str|None): The version string if retrievable.
            - path (str|None): The absolute path to the binary.
    """
    tool_path = shutil.which(cmd)

    if not tool_path:
        return {
            "installed": False,
            "version": None,
            "path": None
        }

    try:
        # Execute the command to get version info
        output = subprocess.check_output(
            [cmd, version_flag],
            text=True,
            stderr=subprocess.STDOUT,
            timeout=3
        ).strip()

        # Extract the first line as the version string to keep it clean
        version_clean = output.split('\n')[0] if output else "Unknown"

        return {
            "installed": True,
            "version": version_clean,
            "path": tool_path
        }
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        # Tool exists but execution failed (e.g., permission error)
        return {
            "installed": True,
            "version": "Error retrieving version",
            "path": tool_path
        }

def check_all() -> Dict[str, Dict[str, Any]]:
    """
    Checks a predefined list of critical development tools using the generic checker.

    Returns:
        Dict[str, Dict[str, Any]]: A map of tool names to their status objects.
    """
    # Mapping logic: Key is the display name, Value is the binary command
    tools_map = {
        "python": "python3",
        "node": "node",
        "npm": "npm",
        "docker": "docker",
        "git": "git"
    }

    results = {}
    for name, binary in tools_map.items():
        results[name] = check_tool_availability(binary)
    
    return results
