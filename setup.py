# core/modules/setup_module.py
import os
import json
import shutil
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

class SetupModule:
    def validate(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        return True, None

    def detect_package_manager(self) -> Optional[str]:
        candidates = {
            "apt": ["apt-get", "--version"],
            "pacman": ["pacman", "--version"],
            "dnf": ["dnf", "--version"],
            "brew": ["brew", "--version"]
        }
        for name, cmd in candidates.items():
            if shutil.which(cmd[0]):
                return name
        return None

    def check_tools(self) -> Dict[str, Dict[str, Any]]:
        tools = {}
        def run_check(cmd):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                return r.returncode == 0, r.stdout.strip()
            except Exception:
                return False, ""
        for name, cmd in {
            "python": ["python3", "--version"],
            "node": ["node", "--version"],
            "npm": ["npm", "--version"],
            "git": ["git", "--version"],
            "docker": ["docker", "--version"]
        }.items():
            ok, out = run_check(cmd)
            tools[name] = {"installed": ok, "version": out or None, "path": shutil.which(cmd[0])}
        return tools

    def create_user_config(self, config_path: str, force: bool=False) -> Dict[str, Any]:
        default = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "settings": {
                "auto_update": True,
                "language": "en",
                "color_output": True
            }
        }
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        if os.path.exists(config_path) and not force:
            with open(config_path, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except Exception:
                    existing = {}
            merged = {**default, **existing}
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=2)
            return {"created": False, "path": config_path}
        else:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
            return {"created": True, "path": config_path}

    def run_installer(self, manager: str, packages: Dict[str, str]) -> Dict[str, Any]:
        results = {}
        if manager is None:
            return {"error": "No package manager detected", "performed": False}
        for key, pkg in packages.items():
            try:
                if manager == "apt":
                    cmd = ["sudo", "apt-get", "install", "-y", pkg]
                elif manager == "pacman":
                    cmd = ["sudo", "pacman", "-S", "--noconfirm", pkg]
                elif manager == "dnf":
                    cmd = ["sudo", "dnf", "install", "-y", pkg]
                elif manager == "brew":
                    cmd = ["brew", "install", pkg]
                else:
                    results[key] = {"ok": False, "error": "unsupported manager"}
                    continue
                r = subprocess.run(cmd, capture_output=True, text=True)
                results[key] = {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr}
            except Exception as e:
                results[key] = {"ok": False, "error": str(e)}
        return {"performed": True, "results": results}

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        dry = bool(args.get("dry_run", False))
        force = bool(args.get("force", False))
        auto = bool(args.get("yes", False))
        user_home = os.path.expanduser("~")
        config_path = os.path.join(user_home, ".devion", "config.json")
        manager = self.detect_package_manager()
        tools = self.check_tools()
        config_res = None
        if dry:
            return {
                "success": True,
                "data": {
                    "dry_run": True,
                    "package_manager": manager,
                    "tools": tools,
                    "config_path": config_path
                },
                "message": "Dry run: setup would create config and check tools.",
                "errors": []
            }
        config_res = self.create_user_config(config_path, force=force)
        missing = {k:v for k,v in tools.items() if not v["installed"]}
        suggestions = {}
        if missing:
            suggestions["missing"] = list(missing.keys())
            suggestions["package_manager"] = manager
            suggestions["commands"] = {}
            if manager == "apt":
                for m in missing:
                    if m == "python":
                        suggestions["commands"][m] = "sudo apt-get install -y python3"
                    elif m == "node":
                        suggestions["commands"][m] = "sudo apt-get install -y nodejs npm"
                    elif m == "docker":
                        suggestions["commands"][m] = "sudo apt-get install -y docker.io"
                    else:
                        suggestions["commands"][m] = f"sudo apt-get install -y {m}"
            elif manager == "pacman":
                for m in missing:
                    suggestions["commands"][m] = f"sudo pacman -S --noconfirm {m}"
            elif manager == "dnf":
                for m in missing:
                    suggestions["commands"][m] = f"sudo dnf install -y {m}"
            elif manager == "brew":
                for m in missing:
                    suggestions["commands"][m] = f"brew install {m}"
            else:
                for m in missing:
                    suggestions["commands"][m] = f"Install {m} via your package manager"
        return {
            "success": True,
            "data": {
                "package_manager": manager,
                "tools": tools,
                "missing": suggestions.get("missing", []),
                "suggestions": suggestions.get("commands", {}),
                "config_result": config_res
            },
            "message": "Setup completed (or simulated).",
            "errors": []
        }
