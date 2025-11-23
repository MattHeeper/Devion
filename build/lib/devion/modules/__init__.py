# devion/modules/__init__.py
"""
The modules package contains all concrete implementations of Devion commands.
Each file in this directory should implement the DevionModuleInterface.
"""

# We explicitly avoid importing concrete modules here to prevent circular dependencies
# and rely on the dynamic loading implemented in cli_bridge.py.
