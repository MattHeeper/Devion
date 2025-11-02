import subprocess
import shutil
from typing import Optional, Dict


def run_command(cmd: list) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        return (result.returncode == 0, result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return (False, "")


def check_python() -> Dict[str, any]:
    success, output = run_command(["python3", "--version"])
    
    if success:
        version = output.replace("Python ", "")
        return {
            "installed": True,
            "version": version,
            "path": shutil.which("python3")
        }
    
    return {
        "installed": False,
        "version": None,
        "path": None
    }


def check_node() -> Dict[str, any]:
    success, output = run_command(["node", "--version"])
    
    if success:
        version = output.replace("v", "")
        return {
            "installed": True,
            "version": version,
            "path": shutil.which("node")
        }
    
    return {
        "installed": False,
        "version": None,
        "path": None
    }


def check_npm() -> Dict[str, any]:
    success, output = run_command(["npm", "--version"])
    
    if success:
        return {
            "installed": True,
            "version": output,
            "path": shutil.which("npm")
        }
    
    return {
        "installed": False,
        "version": None,
        "path": None
    }


def check_docker() -> Dict[str, any]:
    success, output = run_command(["docker", "--version"])
    
    if success:
        version = output.replace("Docker version ", "").split(",")[0]
        return {
            "installed": True,
            "version": version,
            "path": shutil.which("docker")
        }
    
    return {
        "installed": False,
        "version": None,
        "path": None
    }


def check_git() -> Dict[str, any]:
    success, output = run_command(["git", "--version"])
    
    if success:
        version = output.replace("git version ", "")
        return {
            "installed": True,
            "version": version,
            "path": shutil.which("git")
        }
    
    return {
        "installed": False,
        "version": None,
        "path": None
    }


def check_all() -> Dict[str, Dict]:
    return {
        "python": check_python(),
        "node": check_node(),
        "npm": check_npm(),
        "docker": check_docker(),
        "git": check_git()
    }
