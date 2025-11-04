import os
import json
from datetime import datetime

class AnalyzeModule:
    
    def run(self, args=None):
        args = args or {}
        current_dir = os.getcwd()

        file_count = 0
        folder_count = 0
        file_types = {}

        for root, dirs, files in os.walk(current_dir):
            folder_count += len(dirs)
            file_count += len(files)

            for f in files:
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

        return {
            "success": True,
            "data": summary,
            "message": "🧠 Project analysis completed successfully.",
            "errors": []
        }
