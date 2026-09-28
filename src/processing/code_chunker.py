from pathlib import Path


# ==========================================
# CODE CHUNK
# ==========================================

class CodeChunk:
    """
    Represents a meaningful piece of source code.
    """

    def __init__(
        self,
        file_path: Path,
        language: str,
        chunk_type: str,
        name: str,
        start_line: int,
        end_line: int,
        content: str,
    ):

        self.file_path = Path(file_path)
        self.language = language
        self.chunk_type = chunk_type
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.content = content

    def to_dict(self) -> dict:
        """
        Convert the code chunk into a dictionary.
        """

        return {
            "file_path": str(self.file_path),
            "language": self.language,
            "chunk_type": self.chunk_type,
            "name": self.name,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "content": self.content,
        }


# ==========================================
# EXTRACT LINES
# ==========================================

def extract_lines(
    content: str,
    start_line: int,
    end_line: int,
) -> str:
    """
    Extract specific lines from source code.

    Line numbers are 1-based.
    """

    lines = content.splitlines()

    selected_lines = lines[
        start_line - 1 : end_line
    ]

    return "\n".join(selected_lines)


# ==========================================
# CREATE FUNCTION CHUNKS
# ==========================================

def create_function_chunks(
    parsed_code,
    source_content: str,
) -> list[CodeChunk]:

    chunks = []

    for function in parsed_code.functions:

        content = extract_lines(
            source_content,
            function["start_line"],
            function["end_line"],
        )

        chunk = CodeChunk(
            file_path=parsed_code.file_path,
            language=parsed_code.language,
            chunk_type="function",
            name=function["name"],
            start_line=function["start_line"],
            end_line=function["end_line"],
            content=content,
        )

        chunks.append(chunk)

    return chunks


# ==========================================
# CREATE CLASS CHUNKS
# ==========================================

def create_class_chunks(
    parsed_code,
    source_content: str,
) -> list[CodeChunk]:

    chunks = []

    for class_info in parsed_code.classes:

        content = extract_lines(
            source_content,
            class_info["start_line"],
            class_info["end_line"],
        )

        chunk = CodeChunk(
            file_path=parsed_code.file_path,
            language=parsed_code.language,
            chunk_type="class",
            name=class_info["name"],
            start_line=class_info["start_line"],
            end_line=class_info["end_line"],
            content=content,
        )

        chunks.append(chunk)

    return chunks


# ==========================================
# CREATE IMPORT CHUNKS
# ==========================================

def create_import_chunks(
    parsed_code,
    source_content: str,
) -> list[CodeChunk]:

    chunks = []

    for import_info in parsed_code.imports:

        content = extract_lines(
            source_content,
            import_info["start_line"],
            import_info["start_line"],
        )

        chunk = CodeChunk(
            file_path=parsed_code.file_path,
            language=parsed_code.language,
            chunk_type="import",
            name=import_info["name"],
            start_line=import_info["start_line"],
            end_line=import_info["start_line"],
            content=content,
        )

        chunks.append(chunk)

    return chunks


# ==========================================
# CREATE ALL CHUNKS
# ==========================================

def create_code_chunks(
    parsed_code,
    source_content: str,
) -> list[CodeChunk]:
    """
    Create meaningful code chunks from
    parsed source code.
    """

    chunks = []

    # Functions
    chunks.extend(
        create_function_chunks(
            parsed_code,
            source_content,
        )
    )

    # Classes
    chunks.extend(
        create_class_chunks(
            parsed_code,
            source_content,
        )
    )

    # Imports
    chunks.extend(
        create_import_chunks(
            parsed_code,
            source_content,
        )
    )

    return chunks