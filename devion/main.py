import sys
# Import the main execution logic from the bridge interface
from devion.interfaces.cli_bridge import run_cli_bridge

def main() -> None:
    """
    The main entry point for the Python core execution.
    
    When called via 'python3 -m devion.main', it executes the CLI bridge 
    logic to read command and arguments from sys.argv and dispatch the task.
    
    This function should remain minimal and focused on bridge execution.
    """
    run_cli_bridge()

if __name__ == "__main__":
    # Check if we are running as an installed package module
    # The 'devion.main' approach ensures compatibility when installed via pip.
    if sys.argv[0].endswith('__main__.py'):
        main()
    else:
        # Fallback/direct execution support
        main()
