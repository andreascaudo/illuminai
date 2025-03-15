import openai
from .llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    Provider for OpenAI's GPT models.
    """

    def __init__(self):
        """Initialize the OpenAI provider."""
        super().__init__()
        self.api_key = self.get_api_key()

        # Set up the OpenAI client if API key is available
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def process(self, prompt):
        """
        Process a prompt with GPT.

        Args:
            prompt (str): The prompt to process

        Returns:
            str: The GPT response

        Raises:
            Exception: If there's an error processing the prompt
        """
        if not self.api_key:
            raise Exception(
                "OpenAI API key not set. Please configure it in Settings.")

        if not self.client:
            self.client = openai.OpenAI(api_key=self.api_key)

        try:
            # Use GPT-4 Turbo with a moderate max tokens
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response content
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content

            return "No response generated."

        except Exception as e:
            raise Exception(f"Error with OpenAI API: {str(e)}")

    def get_api_key(self):
        """
        Get the OpenAI API key from settings.

        Returns:
            str: The OpenAI API key
        """
        return self.settings.value("openai_api_key", "")

    @classmethod
    def get_name(cls):
        """
        Get the name of this provider.

        Returns:
            str: The provider name
        """
        return "GPT (OpenAI)"
