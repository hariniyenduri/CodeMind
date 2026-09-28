from src.embeddings.embedding_generator import EmbeddingGenerator
from src.rag.retriever import RAGRetriever
from src.rag.context_builder import build_rag_context
from src.llm.prompt_builder import build_codebase_prompt
from src.llm.llm_manager import LLMManager


class RAGEngine:
    """
    Complete CodeMind RAG pipeline.

    Question
        ↓
    Query Embedding
        ↓
    ChromaDB Retrieval
        ↓
    Context Builder
        ↓
    Prompt Builder
        ↓
    LLM Manager
        ↓
    Answer
    """

    def __init__(self):

        self.embedding_generator = (
            EmbeddingGenerator()
        )

        self.retriever = RAGRetriever()

        self.llm_manager = LLMManager()

    def ask(
        self,
        question: str,
        n_results: int = 3,
    ):

        # ======================================
        # 1. Generate query embedding
        # ======================================

        query_embedding = (
            self.embedding_generator.generate_embedding(
                question
            )
        )

        # ======================================
        # 2. Retrieve relevant code chunks
        # ======================================

        retrieved_chunks = self.retriever.retrieve(
            query_embedding=query_embedding,
            n_results=n_results,
        )

        # ======================================
        # 3. Build context
        # ======================================

        context = build_rag_context(
            retrieved_chunks
        )

        # ======================================
        # 4. Build prompt
        # ======================================

        prompt = build_codebase_prompt(
            question=question,
            context=context,
        )

        # ======================================
        # 5. Generate answer
        # ======================================

        result = self.llm_manager.generate(
            prompt,
            max_output_tokens=600,
        )

        return result