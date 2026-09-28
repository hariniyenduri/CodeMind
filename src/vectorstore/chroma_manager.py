import chromadb
from pathlib import Path

from config.settings import CHROMA_DIR


# ==========================================
# CHROMA CONFIGURATION
# ==========================================

COLLECTION_NAME = "codemind_code"


# ==========================================
# CHROMA MANAGER
# ==========================================

class ChromaManager:
    """
    Manages CodeMind's persistent ChromaDB vector store.

    Stores:
    - code embeddings
    - source code chunks
    - file information
    - chunk metadata

    The database location is taken from
    config.settings.CHROMA_DIR.
    """

    def __init__(
        self,
        db_path: Path = CHROMA_DIR,
        collection_name: str = COLLECTION_NAME,
    ):

        self.db_path = Path(db_path)

        # ======================================
        # CREATE DATABASE DIRECTORY
        # ======================================

        self.db_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ======================================
        # CREATE PERSISTENT CHROMA CLIENT
        # ======================================

        self.client = chromadb.PersistentClient(
            path=str(self.db_path)
        )

        # ======================================
        # CREATE OR LOAD COLLECTION
        # ======================================

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    # ==========================================
    # ADD CODE CHUNKS
    # ==========================================

    def add_chunks(
        self,
        chunks,
        embeddings,
    ):
        """
        Store code chunks and their embeddings
        in ChromaDB.
        """

        if not chunks:
            return

        if len(chunks) != len(embeddings):

            raise ValueError(
                "Number of chunks and embeddings "
                "must be the same."
            )

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            # ----------------------------------
            # Unique chunk ID
            # ----------------------------------

            chunk_id = (
                f"{chunk.file_path}_"
                f"{chunk.start_line}_"
                f"{chunk.end_line}_"
                f"{index}"
            )

            ids.append(chunk_id)

            # ----------------------------------
            # Source code
            # ----------------------------------

            documents.append(
                chunk.content
            )

            # ----------------------------------
            # Metadata
            # ----------------------------------

            metadatas.append(
                {
                    "file_path": str(
                        chunk.file_path
                    ),
                    "language": chunk.language,
                    "chunk_type": chunk.chunk_type,
                    "name": chunk.name,
                    "start_line": chunk.start_line,
                    "end_line": chunk.end_line,
                }
            )

        # ======================================
        # STORE IN CHROMADB
        # ======================================

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    # ==========================================
    # SEARCH
    # ==========================================

    def search(
        self,
        query_embedding,
        n_results: int = 5,
    ):
        """
        Find the most relevant code chunks
        for a query embedding.
        """

        total_chunks = self.collection.count()

        # --------------------------------------
        # No stored chunks
        # --------------------------------------

        if total_chunks == 0:

            return {
                "documents": [[]],
                "metadatas": [[]],
                "ids": [[]],
                "distances": [[]],
            }

        # --------------------------------------
        # Do not request more results than exist
        # --------------------------------------

        n_results = min(
            n_results,
            total_chunks,
        )

        # ======================================
        # QUERY CHROMADB
        # ======================================

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=n_results,
        )

        return results

    # ==========================================
    # COUNT
    # ==========================================

    def count(self) -> int:
        """
        Return the number of stored code chunks.
        """

        return self.collection.count()

    # ==========================================
    # CLEAR
    # ==========================================

    def clear(self):
        """
        Remove all code chunks from the
        current ChromaDB collection.
        """

        self.client.delete_collection(
            self.collection.name
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME
            )
        )