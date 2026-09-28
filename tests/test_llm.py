from src.llm.llm_manager import LLMManager


def main():

    print("\n================================")
    print("      CodeMind LLM Test")
    print("================================\n")

    manager = LLMManager()

    prompt = """
You are testing the CodeMind LLM system.

Answer this question in one sentence:

What is the purpose of a Python function?
"""

    result = manager.generate(
        prompt,
        max_output_tokens=100,
    )

    print("\n================================")
    print("Provider Used:")
    print(result["provider"])

    print("\nResponse:")
    print(result["response"])

    print("\n================================")


if __name__ == "__main__":
    main()