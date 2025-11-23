import os
from typing import Dict, List

def list_files_recursively(directory: str, exclude_hidden: bool = True) -> List[str]:
    """
    Recursively lists all files in a directory.

    Args:
        directory (str): The root directory to scan.
        exclude_hidden (bool): If True, skips directories starting with '.'.

    Returns:
        List[str]: A list of absolute file paths.
    """
    file_paths = []
    
    for root, dirs, files in os.walk(directory):
        if exclude_hidden:
            # Modify dirs in-place to skip hidden folders during traversal
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_paths.append(os.path.join(root, file))
            
    return file_paths

def safe_create_dir(path: str) -> bool:
    """
    Creates a directory if it does not exist.

    Args:
        path (str): The directory path.

    Returns:
        bool: True if created or already exists, False on error.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError:
        return False
