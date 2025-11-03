import json

class HelpModule:
    def run(self, args=None):
        """Display available Devion commands and their descriptions."""

        commands = {
            "init": "Initialize Devion and create configuration files.",
            "scan": "Scan your system for development tools and environment status.",
            "analyze": "Analyze the project structure and generate a summary.",
            "fix": "Fix missing tools or configurations automatically.",
            "config": "Display current Devion configuration details.",
            "use": "Activate or switch target environments.",
            "deploy": "Deploy the current project to the output directory.",
            "help": "Show available commands and their descriptions."
        }

        return {
            "success": True,
            "data": {
                "commands": commands
            },
            "message": "📘 Devion command reference loaded successfully.",
            "errors": []
        }
