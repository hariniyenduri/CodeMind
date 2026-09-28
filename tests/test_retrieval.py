from src.rag.retriever import RAGRetriever
from src.embeddings.embedding_generator import EmbeddingGenerator


def main():

    print("\n================================")
    print("       CodeMind RAG Test")
    print("================================\n")

    # -----------------------------------------
    # Initialize components
    # -----------------------------------------

    retriever = RAGRetriever()
    embedding_generator = EmbeddingGenerator()

    # -----------------------------------------
    # Check ChromaDB
    # -----------------------------------------

    total_chunks = retriever.vector_store.count()

    print(
        f"Stored chunks: {total_chunks}"
    )

    if total_chunks == 0:

        print(
            "\nNo chunks are currently stored "
            "in ChromaDB."
        )

        return

    # -----------------------------------------
    # User question
    # -----------------------------------------

    question = "Where is login implemented?"

    print(
        f"\nQuestion: {question}"
    )

    # -----------------------------------------
    # Generate query embedding
    # -----------------------------------------

    query_embedding = (
        embedding_generator.generate_embedding(
            question
        )
    )

    print(
        "\nQuery embedding generated."
    )

    # -----------------------------------------
    # Retrieve relevant chunks
    # -----------------------------------------

    chunks = retriever.retrieve(
        query_embedding=query_embedding,
        n_results=5,
    )

    print(
        f"\nRetrieved {len(chunks)} chunks.\n"
    )

    # -----------------------------------------
    # Display results
    # -----------------------------------------

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        print(
            f"--- RESULT {index} ---"
        )

        print(
            "File:",
            chunk["file"],
        )

        print(
            "Language:",
            chunk["language"],
        )

        print(
            "Type:",
            chunk["type"],
        )

        print(
            "Name:",
            chunk["name"],
        )

        print(
            "Lines:",
            f'{chunk["start_line"]}-'
            f'{chunk["end_line"]}',
        )

        print(
            "Distance:",
            chunk["distance"],
        )

        print(
            "\nCode:"
        )

        print(
            chunk["content"]
        )

        print()


if __name__ == "__main__":
    main()
    