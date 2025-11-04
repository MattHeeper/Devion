
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseModule(ABC):

    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0.0" 

    @abstractmethod
    def validate(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def format_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def get_info(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "version": self.version
        }

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
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
