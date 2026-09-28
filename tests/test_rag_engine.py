from src.rag.rag_engine import RAGEngine


def main():

    print("\n================================")
    print("       CodeMind RAG Engine")
    print("================================\n")

    engine = RAGEngine()

    question = "What is the capital of India?"

    print(
        f"Question: {question}\n"
    )

    print(
        "Generating answer...\n"
    )

    result = engine.ask(
        question
    )

    print(
        "\n================================"
    )

    print(
        "             ANSWER"
    )

    print(
        "================================\n"
    )

    print(
        f"Provider: {result['provider']}"
    )

    print(
        f"\nResponse:\n{result['response']}"
    )


if __name__ == "__main__":
    main()