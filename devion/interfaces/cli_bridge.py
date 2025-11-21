import sys
import json
from typing import Dict, Type, Any

# NOTE: We assume concrete modules exist and import them here.
# These imports will be corrected once the modules are created.
# For now, we will assume a StatusModule exists.
from devion.modules.status_module import StatusModule 

# The command map links CLI command strings to their corresponding Python module class.
COMMAND_MAP: Dict[str, Type[Any]] = {
    "status": StatusModule,
    # "analyze": AnalyzeModule, 
    # Add other commands here as they are implemented
}

def create_standard_response(success: bool, data: Any = None, message: str = "", errors: list = None) -> dict:
    """
    Creates a standardized dictionary response ready for JSON serialization back to the CLI.

    Args:
        success (bool): Indicates if the operation was successful.
        data (Any, optional): The resulting data from the module execution.
        message (str, optional): A brief human-readable message.
        errors (list, optional): A list of specific error details, if any.
        
    Returns:
        dict: The final, structured response object.
    """
    return {
        "success": success,
        "message": message,
        "data": data if data is not None else {},
        "errors": errors if errors is not None else [],
    }

def dispatch_command(command: str, raw_args_json: str) -> None:
    """
    Dispatches the received command to the correct Python module.

    This function is the main execution handler. It handles module lookup, 
    instantiation, execution, and centralized error reporting.

    Args:
        command (str): The command verb received from the CLI (e.g., 'status').
        raw_args_json (str): The raw JSON string containing command arguments.
    """
    try:
        # 1. Deserialize arguments
        args = json.loads(raw_args_json)
        
        # 2. Find the correct module class
        ModuleClass = COMMAND_MAP.get(command)
        
        if not ModuleClass:
            response = create_standard_response(
                success=False, 
                message=f"Error: Unknown command '{command}'.", 
                errors=["Command not defined in the backend COMMAND_MAP."]
            )
        else:
            # 3. Instantiate and execute the module
            module_instance = ModuleClass(args)
            
            # Module execution is wrapped in a try/except for robust error catching
            try:
                module_result = module_instance.run() 
                response = create_standard_response(success=True, data=module_result)
            except Exception as e:
                response = create_standard_response(
                    success=False, 
                    message=f"Execution error in module '{command}'.", 
                    errors=[str(e)]
                )

    except json.JSONDecodeError:
        # Error handling for invalid JSON input from Node.js
        response = create_standard_response(
            success=False, 
            message="Input Error: Invalid JSON arguments received.", 
            errors=["The argument string passed to Python could not be parsed."]
        )
    except Exception as e:
        # Catch any other unexpected exceptions (e.g., unhandled system error)
        response = create_standard_response(
            success=False, 
            message="Internal Dispatch Error.", 
            errors=[str(e)]
        )
        
    # 4. Serialize and print the final response to STDOUT for Node.js
    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()


def run_cli_bridge() -> None:
    """
    Reads input from the command line and initiates command dispatch.

    The Node.js CLI passes command and arguments as sys.argv[1] and sys.argv[2].
    """
    try:
        if len(sys.argv) < 3:
            # This handles cases where arguments were not passed correctly from the CLI
            response = create_standard_response(
                success=False, 
                message="CLI Bridge Error: Command and arguments are missing.",
                errors=["Expected format: python3 -m devion.main <command> <args_json>"]
            )
            sys.stdout.write(json.dumps(response))
            sys.stdout.flush()
            return

        command = sys.argv[1]
        raw_args_json = sys.argv[2]
        
        dispatch_command(command, raw_args_json)

    except Exception as e:
        # Final safety net for critical system errors
        response = create_standard_response(
            success=False, 
            message="Fatal System Error during bridge execution.", 
            errors=[str(e)]
        )
        sys.stdout.write(json.dumps(response))
        sys.stdout.flush()
        
        # Ensure process exits with an error code if possible, though output is already sent
        sys.exit(1)
