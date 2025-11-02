import os
import json
from datetime import datetime

class InitModule:
    def run(self, args=None):
        """Initialize Devion configuration and folders."""
        home_dir = os.path.expanduser("~")
        devion_dir = os.path.join(home_dir, ".devion")
        config_file = os.path.join(devion_dir, "config.json")

        # ساخت پوشه اصلی اگه وجود نداشت
        os.makedirs(devion_dir, exist_ok=True)

        # داده‌های پیش‌فرض تنظیمات
        default_config = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "settings": {
                "auto_update": True,
                "language": "en",
                "color_output": True
            }
        }

        # ذخیره در فایل config.json
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

        return {
            "success": True,
            "data": {"config_path": config_file},
            "message": f"✅ Devion initialized successfully at {config_file}",
            "errors": []
        }
