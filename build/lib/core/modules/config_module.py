import os
import json

class ConfigModule:

    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser("~"), ".devion", "config.json")

    def run(self, args=None):
        if not os.path.exists(self.config_path):
            return {
                "success": False,
                "message": "Config file not found. Please run 'devion init' first.",
                "data": None
            }

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        if not args or len(args) == 0:
            return {
                "success": True,
                "message": "📄 Current Devion configuration loaded successfully.",
                "data": config
            }

        if len(args) >= 2:
            key = args[0]
            value = args[1]

            if key in config["settings"]:
                config["settings"][key] = (
                    value.lower() == "true" if value.lower() in ["true", "false"] else value
                )

                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2)

                return {
                    "success": True,
                    "message": f"✅ Setting '{key}' updated to '{value}'.",
                    "data": config
                }
            else:
                return {
                    "success": False,
                    "message": f"⚠️ Unknown config key: {key}",
                    "data": None
                }

        return {
            "success": False,
            "message": "⚠️ Invalid usage. Example: devion config language fa",
            "data": None
        }
