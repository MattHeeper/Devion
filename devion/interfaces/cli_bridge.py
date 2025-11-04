
import sys
import json
import traceback

from devion.main import handle_command


def read_stdin() -> str:
    try:
        data = sys.stdin.read().strip()
        return data
    except Exception as e:
        print(json.dumps({
            "success": False,
            "data": None,
            "message": "Failed to read stdin",
            "errors": [str(e)]
        }, indent=2))
        sys.exit(1)


def parse_input(raw_data: str):
    if not raw_data:
        return {"command": "", "args": {}}
    
    try:
        parsed = json.loads(raw_data)
        if isinstance(parsed, str):
            return {"command": parsed, "args": {}}
        elif isinstance(parsed, dict):
            return {
                "command": parsed.get("command", ""),
                "args": parsed.get("args", {}) or {}
            }
        else:
            return {"command": "", "args": {}}
    except json.JSONDecodeError:
        return {"command": raw_data.strip(), "args": {}}


def main():
    try:
        raw_data = read_stdin()
        payload = parse_input(raw_data)

        result = handle_command(payload)
        print(json.dumps(result, indent=2))
    except KeyboardInterrupt:
        print(json.dumps({
            "success": False,
            "message": "Execution interrupted by user",
            "data": None,
            "errors": []
        }, indent=2))
        sys.exit(130)
    except Exception as e:
        tb = traceback.format_exc()
        print(json.dumps({
            "success": False,
            "data": None,
            "message": "CLI Bridge internal error",
            "errors": [str(e), tb]
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
