import sys
import json
import traceback
from typing import Dict, Any, Type
import importlib
from devion.interfaces.module_interface import DevionModuleInterface

# ✅ Full Mapping of all supported CLI commands to their Python modules
COMMAND_MAP: Dict[str, str] = {
    "status": "devion.modules.status_module.StatusModule",
    "scan": "devion.modules.scan_module.ScanModule",
    "analyze": "devion.modules.analyze_module.AnalyzeModule",
    "fix": "devion.modules.fix_module.FixModule",
    "deploy": "devion.modules.deploy_module.DeployModule",
    "config": "devion.modules.config_module.ConfigModule",
    "init": "devion.modules.init_module.InitModule",
    "help": "devion.modules.help_module.HelpModule",
    "use": "devion.modules.use_module.UseModule",
}

def load_module_class(module_path: str) -> Type[DevionModuleInterface]:
    """
    Dynamically loads a module class based on its full dotted path string.
    """
    parts = module_path.rsplit(".", 1)
    if len(parts) != 2:
        raise ImportError(f"Invalid module path format: {module_path}")
        
    module_name, class_name = parts
    
    # Use importlib for clean dynamic loading
    module = importlib.import_module(module_name)
    
    module_class = getattr(module, class_name)
    
    if not issubclass(module_class, DevionModuleInterface):
        raise TypeError(f"Module {class_name} does not implement DevionModuleInterface.")
        
    return module_class


def route_command(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Routes the command to the corresponding dynamically loaded module and executes it.
    """
    if command not in COMMAND_MAP:
        return {
            "success": False,
            "data": None,
            "message": f"Error: Unknown command '{command}'.",
            "errors": [f"Command not defined in the backend COMMAND_MAP. Available: {list(COMMAND_MAP.keys())}"],
        }

    try:
        # 1. Dynamically load the module class
        module_class = load_module_class(COMMAND_MAP[command])
        
        # 2. Instantiate the module, passing args to the constructor (__init__)
        module_instance = module_class(args) 
        
        # 3. Execute the module's run method
        result = module_instance.run()
        
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            return {
                "success": False,
                "data": None,
                "message": "Module returned invalid result (not a dict)",
                "errors": [f"Expected dict, got {type(result)}"],
            }
            
        # Ensure base fields exist for consistent API response
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
            "message": f"Module execution failed for '{command}'",
            "errors": [str(e), tb],
        }


def run_cli_bridge() -> None:
    """
    Main function to read arguments from sys.argv, route the command, and print the JSON result.
    """
    if len(sys.argv) < 3:
        result = {
            "success": False,
            "data": None,
            "message": "CLI Bridge Error: Command and arguments are missing.",
            "errors": ["Expected format: python3 -m devion.main <command> <args_json>"],
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    command = sys.argv[1]
    raw_args_json = sys.argv[2]
    args = {}

    try:
        args = json.loads(raw_args_json)
    except json.JSONDecodeError:
        result = {
            "success": False,
            "data": None,
            "message": "Invalid JSON arguments received from CLI",
            "errors": ["Arguments must be a valid JSON string."],
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)
        
    result = route_command(command, args)
    print(json.dumps(result, indent=2))
