import os
from datetime import datetime
from typing import Dict, Any

from devion.interfaces.module_interface import DevionModuleInterface

class AnalyzeModule(DevionModuleInterface):
    """
    Module responsible for analyzing the current project structure, counting 
    files/folders, and categorizing file types within the working directory.
    """

    def __init__(self, args: dict):
        """
        Initializes the Analyze module with command-line arguments.
        """
        super().__init__(args)

    def validate_args(self) -> Dict[str, Any]:
        """
        Validates arguments specific to the analysis module. 
        Currently, it accepts no special flags but is ready for future options 
        like --path or --ignore.
        
        Returns:
            Dict: A dictionary of cleaned and validated arguments.
        """
        # Future validation logic for flags like 'path', 'format', etc., would go here.
        return self.args 

    def execute(self) -> Dict[str, Any]:
        """
        Runs the core analysis logic by recursively walking the current directory.
        
        Returns:
            Dict: The data payload containing the project summary statistics.
        """
        # Determine the directory to scan (default to current working directory)
        # Note: We can expand this later using self.args to respect a user-specified path.
        current_dir = os.getcwd()

        file_count = 0
        folder_count = 0
        file_types: Dict[str, int] = {}

        # Recursively walk the directory tree 
        for root, dirs, files in os.walk(current_dir):
            # Exclude hidden directories from counting (e.g., .git, .devion)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Update counts
            folder_count += len(dirs)
            file_count += len(files)

            for f in files:
                # Get file extension (or 'no_ext' if none exists)
                ext = os.path.splitext(f)[1] or "no_ext"
                file_types[ext] = file_types.get(ext, 0) + 1

        summary = {
            "scanned_at": datetime.now().isoformat(),
            "directory": current_dir,
            "folders": folder_count,
            "files": file_count,
            "file_types": file_types,
            "project_status": "active" if file_count > 0 else "empty"
        }

        # Return the data payload
        return {
            "summary": summary,
            "message": "🧠 Project analysis completed successfully.",
        }
