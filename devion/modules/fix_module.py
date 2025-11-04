import os
import json
import shutil
from datetime import datetime
import subprocess

class FixModule:

    def run(self, args=None):
        home_dir = os.path.expanduser("~")
        devion_dir = os.path.join(home_dir, ".devion")
        config_file = os.path.join(devion_dir, "config.json")

        fixed_items = []
        errors = []

        if not os.path.exists(devion_dir):
            os.makedirs(devion_dir, exist_ok=True)
            fixed_items.append("Created missing .devion directory")

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
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2)
            fixed_items.append("Recreated missing config.json")

        tools = {
            "python": "python3 --version",
            "node": "node --version",
            "npm": "npm --version",
            "git": "git --version"
        }

        missing_tools = []
        for tool, cmd in tools.items():
            try:
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                missing_tools.append(tool)

        if missing_tools:
            errors.append(f"Missing tools: {', '.join(missing_tools)}")
        else:
            fixed_items.append("All required tools are installed")

        return {
            "success": len(errors) == 0,
            "data": {
                "fixed_items": fixed_items,
                "missing_tools": missing_tools,
                "config_path": config_file
            },
            "message": "⚙️ System fix completed successfully." if not errors else "⚠️ Fix completed with some issues.",
            "errors": errors
        }
