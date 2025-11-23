from abc import ABC, abstractmethod

class DevionModuleInterface(ABC):
    """
    Abstract Base Class (ABC) for all Devion backend modules.

    All core logic modules (e.g., status, analyze, deploy) must inherit 
    from this class and implement the abstract methods to ensure consistent
    execution flow and argument validation.
    """

    def __init__(self, args: dict):
        """
        Initializes the module with arguments passed from the Node.js CLI.
        
        Args:
            args (dict): Dictionary of options/arguments received from the CLI.
        """
        self.args = args

    @abstractmethod
    def validate_args(self) -> dict:
        """
        Validates the arguments received by the module.

        This method must be implemented by concrete modules to ensure all 
        required arguments are present and correctly formatted before execution.

        Returns:
            dict: A clean dictionary of validated arguments ready for execution.
            
        Raises:
            ValueError: If any required argument is missing or invalid.
        """
        pass

    @abstractmethod
    def execute(self) -> dict:
        """
        Contains the main logic of the module.

        This method is where the module performs its core task (e.g., running 
        system checks, analyzing files, or deploying).

        Returns:
            dict: The standardized result dictionary containing 'status', 'data', 
                  and 'message' fields for JSON serialization.
        """
        pass

    def run(self) -> dict:
        """
        Executes the module lifecycle: validation followed by execution.

        This method should be called externally by the CLI bridge.
        """
        # Step 1: Validate arguments before proceeding
        self.validate_args() 
        
        # Step 2: Execute the core logic
        return self.execute()
