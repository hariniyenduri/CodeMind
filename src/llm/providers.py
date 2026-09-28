import os

from dotenv import load_dotenv
from google import genai
from openai import OpenAI


load_dotenv()


class LLMProviderError(Exception):
    """Raised when an LLM provider cannot generate a response."""
    pass


# =========================================================
# GEMINI
# =========================================================

class GeminiProvider:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise LLMProviderError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.8-flash"


    def generate(
        self,
        prompt: str,
        max_output_tokens: int = 1024,
    ) -> str:

        try:

            interaction = self.client.interactions.create(
                model=self.model,
                input=prompt,
            )

            if not interaction.output_text:
                raise LLMProviderError(
                    "Gemini returned an empty response."
                )

            return interaction.output_text

        except Exception as error:

            raise LLMProviderError(
                f"Gemini failed: {error}"
            ) from error


# =========================================================
# GROQ
# =========================================================

class GroqProvider:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise LLMProviderError(
                "GROQ_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = "openai/gpt-oss-120b"


    def generate(
        self,
        prompt: str,
        max_output_tokens: int = 1024,
    ) -> str:

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=max_output_tokens,
            )

            content = response.choices[0].message.content

            if not content:
                raise LLMProviderError(
                    "Groq returned an empty response."
                )

            return content

        except Exception as error:

            raise LLMProviderError(
                f"Groq failed: {error}"
            ) from error


# =========================================================
# OPENROUTER
# =========================================================

class OpenRouterProvider:

    def __init__(self):

        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise LLMProviderError(
                "OPENROUTER_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-oss-120b:free",
        )


    def generate(
        self,
        prompt: str,
        max_output_tokens: int = 1024,
    ) -> str:

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=max_output_tokens,
            )

            content = response.choices[0].message.content

            if not content:
                raise LLMProviderError(
                    "OpenRouter returned an empty response."
                )

            return content

        except Exception as error:

            raise LLMProviderError(
                f"OpenRouter failed: {error}"
            ) from error