from typing import List, Dict


def build_rag_context(
    retrieved_chunks: List[Dict],
) -> str:
    """
    Convert retrieved code chunks into a structured
    context that can be given to the LLM.
    """

    if not retrieved_chunks:
        return "No relevant code was found."

    context_parts = []

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1,
    ):

        file_name = chunk.get(
            "file",
            "Unknown file",
        )

        language = chunk.get(
            "language",
            "Unknown",
        )

        chunk_type = chunk.get(
            "type",
            "code",
        )

        name = chunk.get(
            "name",
            "",
        )

        start_line = chunk.get(
            "start_line",
            "?",
        )

        end_line = chunk.get(
            "end_line",
            "?",
        )

        content = chunk.get(
            "content",
            "",
        )

        context_parts.append(
            f"""
--- CODE CHUNK {index} ---

File: {file_name}
Language: {language}
Type: {chunk_type}
Name: {name}
Lines: {start_line}-{end_line}

Code:
{content}
"""
        )

    return "\n".join(context_parts)