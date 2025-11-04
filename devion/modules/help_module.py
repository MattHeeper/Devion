class HelpModule:
    def run(self, args):
        commands = {
            "init": "Initialize a new Devion project.",
            "scan": "Scan the environment for issues.",
            "analyze": "Analyze detected issues.",
            "fix": "Automatically fix common issues.",
            "config": "Manage project configuration.",
            "use": "Switch between Devion modes or templates.",
            "deploy": "Deploy your project.",
            "help": "Show available commands and usage."
        }

        return {
            "success": True,
            "data": {"commands": commands},
            "message": "📘 Devion command reference loaded successfully.",
            "errors": []
        }
