from abc import ABC, abstractmethod
from PyQt6.QtCore import QSettings


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All LLM providers must implement this interface to provide
    a standardized way to process prompts with different LLM services.
    """

    def __init__(self):
        """Initialize the LLM provider."""
        self.settings = QSettings()

    @abstractmethod
    def process(self, prompt):
        """
        Process a prompt with the LLM.

        Args:
            prompt (str): The prompt to process

        Returns:
            str: The LLM response

        Raises:
            Exception: If there's an error processing the prompt
        """
        pass

    def get_api_key(self):
        """
        Get the API key for this provider from settings.

        Returns:
            str: The API key
        """
        return ""

    @classmethod
    def get_name(cls):
        """
        Get the name of this provider.

        Returns:
            str: The provider name
        """
        return "Base LLM Provider"
