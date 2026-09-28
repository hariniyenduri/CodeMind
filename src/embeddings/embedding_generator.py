from sentence_transformers import SentenceTransformer


# ==========================================
# EMBEDDING MODEL
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingGenerator:
    """
    Generates embeddings for CodeMind code chunks
    and user queries.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
    ):

        self.model_name = model_name

        print(
            f"Loading embedding model: "
            f"{self.model_name}"
        )

        self.model = SentenceTransformer(
            self.model_name
        )

        print(
            "Embedding model loaded successfully."
        )


    # ======================================
    # SINGLE TEXT
    # ======================================

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()


    # ======================================
    # MULTIPLE TEXTS
    # ======================================

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings.tolist()