#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# مسیر فایل: core/interfaces/module_interface.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseModule(ABC):
    """
    پایه برای تمام ماژول‌ها که باید برای هر ماژول پیاده‌سازی بشه.
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0.0"  # می‌تونید ورژن رو تغییر بدید

    @abstractmethod
    def validate(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        برای اعتبارسنجی ورودی‌ها استفاده میشه.
        اگه ورودی‌ها درست نباشه، می‌تونید پیغام خطا بدهید.
        """
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        اجرا کردن دستور یا عملکرد اصلی ماژول.
        این تابع نتیجه‌ی اصلی دستور رو برمی‌گردونه.
        """
        pass

    @abstractmethod
    def format_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        قالب‌بندی و فرمت کردن خروجی به شکل دلخواه
        مثل تبدیل به JSON یا فرمت‌های دیگر
        """
        pass

    def get_info(self) -> Dict[str, str]:
        """
        برای گرفتن اطلاعات پایه‌ای مثل اسم و ورژن
        """
        return {
            "name": self.name,
            "version": self.version
        }

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        این متد کنترل کلیه فرآیندها رو انجام می‌ده.
        ابتدا ورودی رو اعتبارسنجی می‌کنه، بعد عملیات رو اجرا می‌کنه
        و در نهایت خروجی رو فرمت می‌کنه.
        """
        is_valid, error = self.validate(args)

        if not is_valid:
            return {
                "success": False,
                "data": None,
                "message": "Validation failed",
                "errors": [error]
            }

        try:
            result = self.execute(args)
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": "Execution failed",
                "errors": [str(e)]
            }

        try:
            formatted_result = self.format_output(result)
            return formatted_result
        except Exception as e:
            result["errors"].append(f"Formatting error: {str(e)}")
            return result
