from pathlib import Path


# ==========================================
# CODE FILE OBJECT
# ==========================================

class CodeFile:
    """
    Represents a source-code file loaded by CodeMind.
    """

    def __init__(
        self,
        file_path: Path,
        content: str,
    ):
        self.file_path = Path(file_path)
        self.content = content
        self.language = self._detect_language()

    def _detect_language(self) -> str:
        """
        Detect programming language from file extension.
        """

        extension = self.file_path.suffix.lower()

        language_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".jsx": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".java": "Java",
            ".c": "C",
            ".cpp": "C++",
            ".h": "C",
            ".hpp": "C++",
            ".cs": "C#",
            ".go": "Go",
            ".rs": "Rust",
            ".php": "PHP",
            ".rb": "Ruby",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".kts": "Kotlin",
            ".html": "HTML",
            ".css": "CSS",
            ".sql": "SQL",
        }

        return language_map.get(
            extension,
            "Unknown",
        )

    def to_dict(self) -> dict:
        """
        Convert the CodeFile object into a dictionary.
        """

        return {
            "file_path": str(self.file_path),
            "language": self.language,
            "content": self.content,
        }


# ==========================================
# LOAD SINGLE FILE
# ==========================================

def load_file(file_path: Path) -> CodeFile:
    """
    Read a single source-code file.
    """

    file_path = Path(file_path)

    try:

        content = file_path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        content = file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    return CodeFile(
        file_path=file_path,
        content=content,
    )


# ==========================================
# LOAD PROJECT FILES
# ==========================================

def load_project(
    source_files: list[Path],
) -> list[CodeFile]:
    """
    Load all detected source files.
    """

    loaded_files = []

    for file_path in source_files:

        try:

            code_file = load_file(file_path)

            loaded_files.append(code_file)

        except Exception as error:

            print(
                f"Could not load {file_path}: {error}"
            )

    return loaded_files