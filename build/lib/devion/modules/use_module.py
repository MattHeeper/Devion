from datetime import datetime
from typing import Dict, Any

from devion.interfaces.module_interface import DevionModuleInterface

class UseModule(DevionModuleInterface):
    """
    Module responsible for activating a specific target configuration or environment mode.
    This allows users to switch contexts (e.g., 'default', 'production', 'testing').
    """

    def __init__(self, args: dict):
        """
        Initializes the Use module with arguments.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates the arguments.
        
        Returns:
            Dict: The arguments dictionary.
        """
        # Ensure 'target' is treated as a string if present.
        # If specific validation logic for target names is needed, it goes here.
        if 'target' in self.args and not isinstance(self.args['target'], str):
             raise ValueError("The 'target' argument must be a string.")
             
        return self.args

    def execute(self) -> Dict[str, Any]:
        """
        Activates the specified target.
        
        Returns:
            Dict: The data payload containing activation details.
        """
        # specific logic to 'use' a target.
        # Defaults to 'default' if no target is provided.
        target = self.args.get("target", "default")

        result = {
            "activated_at": datetime.now().isoformat(),
            "target": target,
            "status": "active",
        }

        return {
            "data": result,
            "message": f"🎯 Target '{target}' activated successfully."
        }
