# core/modules/scan_module.py
import os
import shutil
import platform
import subprocess
import json

class ScanModule:
    """اسکن کامل سیستم و بررسی ابزارها و مسیرهای اصلی Devion"""

    def run(self, args=None):
        args = args or {}

        tools = {
            "python": self._check_tool("python3", ["--version"]),
            "node": self._check_tool("node", ["--version"]),
            "npm": self._check_tool("npm", ["--version"]),
            "git": self._check_tool("git", ["--version"]),
            "docker": self._check_tool("docker", ["--version"]),
        }

        devion_dir = os.path.expanduser("~/.devion")
        exists = os.path.exists(devion_dir)

        result = {
            "system": {
                "os": platform.system(),
                "release": platform.release(),
                "arch": platform.machine(),
            },
            "tools": tools,
            "devion_folder": {
                "exists": exists,
                "path": devion_dir,
                "files": os.listdir(devion_dir) if exists else [],
            },
        }

        return {
            "success": True,
            "data": result,
            "message": "🔍 System scan completed successfully.",
            "errors": [],
        }

    def _check_tool(self, cmd, args):
        path = shutil.which(cmd)
        if not path:
            return {"installed": False, "version": None, "path": None}

        try:
            output = subprocess.check_output([cmd] + args, text=True).strip()
            return {"installed": True, "version": output, "path": path}
        except Exception as e:
            return {"installed": True, "version": "unknown", "path": path, "error": str(e)}
