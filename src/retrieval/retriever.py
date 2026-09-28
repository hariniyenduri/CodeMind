from src.vectorstore.chroma_manager import ChromaManager


class RAGRetriever:
    """
    Retrieves relevant code chunks from ChromaDB
    and converts them into a format suitable
    for the RAG context builder.
    """

    def __init__(self):

        self.vector_store = ChromaManager()


    def retrieve(
        self,
        query_embedding,
        n_results: int = 5,
    ):
        """
        Search ChromaDB using the query embedding.
        """

        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n_results,
        )

        retrieved_chunks = []

        documents = results.get(
            "documents",
            [[]],
        )

        metadatas = results.get(
            "metadatas",
            [[]],
        )

        if not documents or not documents[0]:
            return retrieved_chunks

        documents = documents[0]
        metadatas = metadatas[0]

        for document, metadata in zip(
            documents,
            metadatas,
        ):

            retrieved_chunks.append(
                {
                    "file": metadata.get(
                        "file_path",
                        "Unknown file",
                    ),

                    "language": metadata.get(
                        "language",
                        "Unknown",
                    ),

                    "type": metadata.get(
                        "chunk_type",
                        "code",
                    ),

                    "name": metadata.get(
                        "name",
                        "",
                    ),

                    "start_line": metadata.get(
                        "start_line",
                        "?",
                    ),

                    "end_line": metadata.get(
                        "end_line",
                        "?",
                    ),

                    "content": document,
                }
            )

        return retrieved_chunks