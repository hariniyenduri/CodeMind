from src.vectorstore.chroma_manager import ChromaManager


class RAGRetriever:
    """
    Retrieves relevant code chunks from ChromaDB
    and preserves similarity distance information.
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

        Returns:
        - retrieved code chunks
        - distance for each retrieved chunk
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

        distances = results.get(
            "distances",
            [[]],
        )

        if not documents or not documents[0]:
            return retrieved_chunks

        documents = documents[0]
        metadatas = metadatas[0]

        if distances and distances[0]:
            distances = distances[0]
        else:
            distances = [None] * len(documents)

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
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

                    # ChromaDB distance
                    "distance": distance,
                }
            )

        return retrieved_chunks