# ==========================================
# CODEMIND RELEVANCE CHECKER
# ==========================================

from typing import List, Dict


# Minimum number of retrieved chunks required
# before considering the question relevant.
MIN_RELEVANT_CHUNKS = 1


def is_project_relevant(
    retrieved_chunks: List[Dict],
) -> bool:
    """
    Determine whether the user's question has
    relevant information in the uploaded project.

    The decision is based on semantic retrieval.
    If no relevant code chunks are retrieved,
    the question is treated as unrelated.
    """

    if not retrieved_chunks:
        return False

    return len(retrieved_chunks) >= MIN_RELEVANT_CHUNKS


def get_irrelevant_response() -> str:
    """
    Return a short response for questions that
    are unrelated to the uploaded project.
    """

    return "This question is not relevant to the uploaded project."