
from typing import Dict, Any, Optional
import sys
import os

# مسیر‌دهی برای ایمپورت داخلی
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from devion.interfaces.module_interface import BaseModule
from devion.utils.system_check import check_all


class StatusModule(BaseModule):

    def validate(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        return True, None

    def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        verbose = args.get("verbose", False)

        tools = check_all()

        installed_count = sum(1 for t in tools.values() if t["installed"])
        total_count = len(tools)

        return {
            "success": True,
            "data": {
                "tools": tools,
                "summary": {
                    "installed": installed_count,
                    "total": total_count,
                    "missing": total_count - installed_count,
                },
            },
            "message": f"{installed_count}/{total_count} tools installed",
            "errors": [],
        }

    def format_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        قالب‌بندی خروجی برای نمایش زیباتر
        """
        if not result.get("success"):
            return result

        tools = result["data"]["tools"]
        formatted_tools = {}

        for name, info in tools.items():
            if info["installed"]:
                formatted_tools[name] = f"✅ {info['version']}"
            else:
                formatted_tools[name] = "❌ Not installed"

        result["data"]["formatted"] = formatted_tools

        return result
