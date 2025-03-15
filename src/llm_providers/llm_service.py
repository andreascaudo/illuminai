import requests
import json
from PyQt6.QtCore import QSettings
from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider
from .xai_provider import XAIProvider


class LLMService:
    """
    Service for managing different LLM providers.
    """

    def __init__(self, provider_name=None):
        """
        Initialize the LLM service.

        Args:
            provider_name (str, optional): The name of the LLM provider to use.
                If None, the default provider from settings will be used.
        """
        self.settings = QSettings()

        # If no provider specified, use the default from settings
        if provider_name is None:
            provider_index = self.settings.value(
                "default_llm_provider", 0, type=int)
            if provider_index == 0:
                provider_name = "Claude (Anthropic)"
            elif provider_index == 1:
                provider_name = "GPT (OpenAI)"
            elif provider_index == 2:
                provider_name = "Grok (xAI)"
            else:
                provider_name = "Claude (Anthropic)"  # Fallback

        # Initialize the appropriate provider
        if "Claude" in provider_name:
            self.provider = AnthropicProvider()
        elif "GPT" in provider_name:
            self.provider = OpenAIProvider()
        elif "Grok" in provider_name:
            self.provider = XAIProvider()
        else:
            # Default to Anthropic
            self.provider = AnthropicProvider()

    def process(self, prompt):
        """
        Process a prompt with the current LLM provider.

        Args:
            prompt (str): The prompt to process

        Returns:
            str: The LLM response

        Raises:
            Exception: If there's an error processing the prompt
        """
        try:
            return self.provider.process(prompt)
        except Exception as e:
            raise Exception(f"Error processing prompt: {str(e)}")

    @staticmethod
    def get_providers():
        """
        Get a list of supported LLM providers.

        Returns:
            list: A list of supported provider names
        """
        return ["Claude (Anthropic)", "GPT (OpenAI)", "Grok (xAI)"]
