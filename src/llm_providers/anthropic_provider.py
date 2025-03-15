import anthropic
from .llm_provider import LLMProvider


class AnthropicProvider(LLMProvider):
    """
    Provider for Anthropic's Claude LLM.
    """

    def __init__(self):
        """Initialize the Anthropic provider."""
        super().__init__()
        self.api_key = self.get_api_key()

        # Default to Claude Sonnet if API key is available
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def process(self, prompt):
        """
        Process a prompt with Claude.

        Args:
            prompt (str): The prompt to process

        Returns:
            str: The Claude response

        Raises:
            Exception: If there's an error processing the prompt
        """
        if not self.api_key:
            raise Exception(
                "Anthropic API key not set. Please configure it in Settings.")

        if not self.client:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        try:
            # Use Claude Sonnet with a moderate max tokens
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract text content from the response
            if response.content:
                for content_block in response.content:
                    if content_block.type == "text":
                        return content_block.text

            return "No response generated."

        except Exception as e:
            raise Exception(f"Error with Anthropic API: {str(e)}")

    def get_api_key(self):
        """
        Get the Anthropic API key from settings.

        Returns:
            str: The Anthropic API key
        """
        return self.settings.value("anthropic_api_key", "")

    @classmethod
    def get_name(cls):
        """
        Get the name of this provider.

        Returns:
            str: The provider name
        """
        return "Claude (Anthropic)"
