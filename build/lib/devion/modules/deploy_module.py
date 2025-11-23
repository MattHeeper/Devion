import os
import json
from datetime import datetime
from typing import Dict, Any

from devion.interfaces.module_interface import DevionModuleInterface

class DeployModule(DevionModuleInterface):
    """
    Module responsible for packaging and deploying the project.
    It creates a deployment output directory ('dist/') and logs the deployment details.
    """

    def __init__(self, args: dict):
        """
        Initializes the Deploy module. Arguments (args) might include deployment targets or flags.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments specific to the deployment process.
        
        Returns:
            Dict: Validated and cleaned arguments.
        """
        # Future validation logic for flags like 'target', 'environment', or 'compress' would go here.
        return self.args 

    def execute(self) -> Dict[str, Any]:
        """
        Runs the core deployment logic: creates the output directory and generates a deployment log.
        
        Returns:
            Dict: The data payload containing the deployment status and details.
        """
        project_dir = os.getcwd()
        # Define the default output directory
        deploy_dir = os.path.join(project_dir, "dist")

        # 1. Create the deployment output directory
        try:
            os.makedirs(deploy_dir, exist_ok=True)
        except OSError as e:
            raise IOError(f"Failed to create deployment directory at {deploy_dir}: {e}")

        log_path = os.path.join(deploy_dir, "deploy_log.json")
        
        # Count items in the project directory (excluding the deployment folder itself for accuracy)
        all_items = os.listdir(project_dir)
        files_packaged = len([item for item in all_items if item != "dist" and not item.startswith('.')])
        
        deploy_info = {
            "deployed_at": datetime.now().isoformat(),
            "project_path": project_dir,
            "output_path": deploy_dir,
            "status": "success",
            "files_packaged": files_packaged,
            # Placeholder for potential steps like 'zip_status', 'upload_status'
        }

        # 2. Write the deployment log
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(deploy_info, f, indent=2)
        except Exception as e:
             raise IOError(f"Failed to write deployment log to {log_path}: {e}")

        # Return the data payload
        return {
            "deployment_info": deploy_info,
            "message": "🚀 Project deployed successfully.",
        }
