from pathlib import Path

from src.processing.code_parser import parse_code_file
from src.processing.code_chunker import create_code_chunks


sample_code = """
import os

def login(username, password):
    if username == "admin":
        return True

    return False


def logout(username):
    return True


class User:

    def __init__(self, username):
        self.username = username
"""


# ==========================================
# PARSE
# ==========================================

parsed = parse_code_file(
    Path("auth.py"),
    sample_code,
    "Python",
)


# ==========================================
# CREATE CHUNKS
# ==========================================

chunks = create_code_chunks(
    parsed,
    sample_code,
)


# ==========================================
# DISPLAY CHUNKS
# ==========================================

print("\n========== CODE CHUNKS ==========")

for index, chunk in enumerate(
    chunks,
    start=1,
):

    print(
        f"\n--- CHUNK {index} ---"
    )

    print(
        f"File: {chunk.file_path}"
    )

    print(
        f"Language: {chunk.language}"
    )

    print(
        f"Type: {chunk.chunk_type}"
    )

    print(
        f"Name: {chunk.name}"
    )

    print(
        f"Lines: "
        f"{chunk.start_line}-"
        f"{chunk.end_line}"
    )

    print("\nContent:")

    print(chunk.content)