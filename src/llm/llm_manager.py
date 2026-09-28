from src.llm.providers import (
    GeminiProvider,
    GroqProvider,
    OpenRouterProvider,
    LLMProviderError,
)


class LLMManager:

    def __init__(self):

        self.providers = []

        # ==========================================
        # PROVIDER 1 — GEMINI
        # ==========================================

        try:
            self.providers.append(
                (
                    "Gemini",
                    GeminiProvider(),
                )
            )
        except LLMProviderError:
            pass


        # ==========================================
        # PROVIDER 2 — GROQ
        # ==========================================

        try:
            self.providers.append(
                (
                    "Groq",
                    GroqProvider(),
                )
            )
        except LLMProviderError:
            pass


        # ==========================================
        # PROVIDER 3 — OPENROUTER
        # ==========================================

        try:
            self.providers.append(
                (
                    "OpenRouter",
                    OpenRouterProvider(),
                )
            )
        except LLMProviderError:
            pass


        if not self.providers:

            raise RuntimeError(
                "No LLM providers are configured."
            )


    def generate(
        self,
        prompt: str,
        max_output_tokens: int = 1024,
    ):

        errors = []

        # ==========================================
        # SEQUENTIAL FALLBACK
        # ==========================================

        for provider_name, provider in self.providers:

            try:

                print(
                    f"Trying LLM provider: "
                    f"{provider_name}"
                )

                response = provider.generate(
                    prompt,
                    max_output_tokens,
                )

                return {
                    "provider": provider_name,
                    "response": response,
                    "errors": errors,
                }

            except LLMProviderError as error:

                print(
                    f"{provider_name} failed."
                )

                errors.append(
                    {
                        "provider": provider_name,
                        "error": str(error),
                    }
                )


        # ==========================================
        # ALL PROVIDERS FAILED
        # ==========================================

        raise RuntimeError(
            "All configured LLM providers failed.\n"
            f"Details: {errors}"
        )