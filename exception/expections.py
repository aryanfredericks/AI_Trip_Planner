class TravelPlannerError(Exception):
    """Base exception for all Travel Planner errors"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


# Specific exceptions inherit from the base
class ConfigNotFoundError(TravelPlannerError):
    """Raised when config.yaml is missing or unreadable"""
    pass


class ModelLoadError(TravelPlannerError):
    """Raised when the LLM fails to load"""
    pass


class AgentExecutionError(TravelPlannerError):
    """Raised when the agent graph fails during execution"""
    pass


class DocumentSaveError(TravelPlannerError):
    """Raised when saving the markdown file fails"""
    pass


class InvalidProviderError(TravelPlannerError):
    """Raised when an unsupported model provider is specified"""
    pass