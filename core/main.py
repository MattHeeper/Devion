
import sys
import json
import traceback
from typing import Dict, Any

COMMAND_MAP = {
    "status": "core.modules.status_module.StatusModule",
    "init": "core.modules.init_module.InitModule",
    "scan": "core.modules.scan_module.ScanModule",
    "analyze": "core.modules.analyze_module.AnalyzeModule",
    "fix": "core.modules.fix_module.FixModule",
    "config": "core.modules.config_module.ConfigModule",
    "use": "core.modules.use_module.UseModule",
    "deploy": "core.modules.deploy_module.DeployModule",
    "help": "core.modules.help_module.HelpModule",
}



def load_module(module_path: str):
    parts = module_path.split(".")
    module_name = ".".join(parts[:-1])
    class_name = parts[-1]
    module = __import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)


def route_command(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if command not in COMMAND_MAP:
        return {
            "success": False,
            "data": None,
            "message": f"Unknown command: {command}",
            "errors": [f"Available commands: {', '.join(COMMAND_MAP.keys())}"],
        }

    try:
        module_class = load_module(COMMAND_MAP[command])
        module_instance = module_class()
        result = module_instance.run(args)
        if not isinstance(result, dict):
            return {
                "success": False,
                "data": None,
                "message": "Module returned invalid result (not a dict)",
                "errors": [],
            }
        # اطمینان از وجود فیلدهای پایه
        result.setdefault("success", True)
        result.setdefault("data", None)
        result.setdefault("message", "")
        result.setdefault("errors", [])
        return result
    except Exception as e:
        tb = traceback.format_exc()
        return {
            "success": False,
            "data": None,
            "message": "Module execution failed",
            "errors": [str(e), tb],
        }


def handle_command(payload: Any) -> Dict[str, Any]:
    try:
        if isinstance(payload, dict):
            command = payload.get("command", "")
            args = payload.get("args", {}) or {}
        elif isinstance(payload, str):
            command = payload
            args = {}
        else:
            return {
                "success": False,
                "data": None,
                "message": "Invalid payload type for handle_command",
                "errors": [f"Expected dict or str, got {type(payload)}"],
            }

        command = str(command).lower()
        return route_command(command, args)
    except Exception as e:
        tb = traceback.format_exc()
        return {
            "success": False,
            "data": None,
            "message": "handle_command error",
            "errors": [str(e), tb],
        }


def _cli_main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "success": False,
                    "data": None,
                    "message": "No command provided",
                    "errors": ["Usage: python -m core.main <command> [args_as_json]"],
                },
                indent=2,
            )
        )
        sys.exit(1)

    command = sys.argv[1]
    args = {}
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(
                json.dumps(
                    {
                        "success": False,
                        "data": None,
                        "message": "Invalid JSON arguments",
                        "errors": ["Arguments must be valid JSON"],
                    },
                    indent=2,
                )
            )
            sys.exit(1)

    result = route_command(command, args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    _cli_main()

