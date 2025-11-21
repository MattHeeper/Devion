# devion/modules/setup_module.py

import subprocess
import platform
from typing import Dict, Any

class SetupModule:
    
    def run(self, args=None):
        args = args or {}
        target_tool = args.get("tool", "all")
        
        os_type = platform.system().lower()
        
        if os_type == "linux":
            return self._setup_linux(target_tool)
        elif os_type == "darwin":
            return self._setup_macos(target_tool)
        else:
            return {
                "success": False,
                "message": f"Unsupported OS: {os_type}",
                "data": None,
                "errors": []
            }
    
    def _setup_linux(self, tool):
        package_manager = self._detect_package_manager()
        
        commands = {
            "node": f"{package_manager['install']} nodejs",
            "npm": f"{package_manager['install']} npm",
            "docker": f"{package_manager['install']} docker.io",
            "python": f"{package_manager['install']} python3",
            "git": f"{package_manager['install']} git"
        }
        
        if tool == "all":
            installed = []
            failed = []
            
            for tool_name, cmd in commands.items():
                try:
                    subprocess.run(cmd, shell=True, check=True)
                    installed.append(tool_name)
                except:
                    failed.append(tool_name)
            
            return {
                "success": len(failed) == 0,
                "data": {
                    "installed": installed,
                    "failed": failed
                },
                "message": f"Setup completed: {len(installed)} installed",
                "errors": failed
            }
        else:
            # نصب یک ابزار خاص
            if tool in commands:
                try:
                    subprocess.run(commands[tool], shell=True, check=True)
                    return {
                        "success": True,
                        "data": {"tool": tool},
                        "message": f"✅ {tool} installed successfully",
                        "errors": []
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "data": None,
                        "message": f"Failed to install {tool}",
                        "errors": [str(e)]
                    }
    
    def _detect_package_manager(self):
        managers = [
            {"name": "apt", "install": "sudo apt-get install -y"},
            {"name": "pacman", "install": "sudo pacman -S --noconfirm"},
            {"name": "dnf", "install": "sudo dnf install -y"},
        ]
        
        for pm in managers:
            try:
                subprocess.run(f"which {pm['name']}", shell=True, check=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return pm
            except:
                continue
        
        return {"name": "unknown", "install": ""}
    
    def _setup_macos(self, tool):
        # برای macOS از brew استفاده می‌کنیم
        commands = {
            "node": "brew install node",
            "npm": "brew install npm",
            "docker": "brew install --cask docker",
            "python": "brew install python3",
            "git": "brew install git"
        }
        
        # مشابه _setup_linux
        # ...