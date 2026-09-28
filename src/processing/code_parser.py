import ast
from pathlib import Path


# ==========================================
# PARSED CODE OBJECT
# ==========================================

class ParsedCode:
    """
    Stores structural information extracted
    from a source-code file.
    """

    def __init__(
        self,
        file_path: Path,
        language: str,
    ):
        self.file_path = Path(file_path)
        self.language = language

        self.functions = []
        self.classes = []
        self.imports = []


# ==========================================
# PYTHON PARSER
# ==========================================

def parse_python_file(
    file_path: Path,
    content: str,
) -> ParsedCode:
    """
    Parse Python source code using AST.
    """

    parsed_code = ParsedCode(
        file_path=file_path,
        language="Python",
    )

    try:

        tree = ast.parse(content)

    except SyntaxError as error:

        print(
            f"Could not parse {file_path}: {error}"
        )

        return parsed_code

    # --------------------------------------
    # Walk through AST
    # --------------------------------------

    for node in ast.walk(tree):

        # ----------------------------------
        # Functions
        # ----------------------------------

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):

            parsed_code.functions.append(
                {
                    "name": node.name,
                    "type": "function",
                    "start_line": node.lineno,
                    "end_line": getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                }
            )

        # ----------------------------------
        # Classes
        # ----------------------------------

        elif isinstance(
            node,
            ast.ClassDef,
        ):

            parsed_code.classes.append(
                {
                    "name": node.name,
                    "type": "class",
                    "start_line": node.lineno,
                    "end_line": getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),
                }
            )

        # ----------------------------------
        # Normal imports
        # ----------------------------------

        elif isinstance(
            node,
            ast.Import,
        ):

            for alias in node.names:

                parsed_code.imports.append(
                    {
                        "name": alias.name,
                        "type": "import",
                        "start_line": node.lineno,
                    }
                )

        # ----------------------------------
        # From imports
        # ----------------------------------

        elif isinstance(
            node,
            ast.ImportFrom,
        ):

            module = node.module or ""

            for alias in node.names:

                import_name = (
                    f"{module}.{alias.name}"
                    if module
                    else alias.name
                )

                parsed_code.imports.append(
                    {
                        "name": import_name,
                        "type": "from_import",
                        "start_line": node.lineno,
                    }
                )

    return parsed_code


# ==========================================
# GENERAL CODE PARSER
# ==========================================

def parse_code_file(
    file_path: Path,
    content: str,
    language: str,
) -> ParsedCode:
    """
    Select the appropriate parser based
    on programming language.
    """

    if language == "Python":

        return parse_python_file(
            file_path,
            content,
        )

    # --------------------------------------
    # Other language parsers will be added
    # later using Tree-sitter.
    # --------------------------------------

    return ParsedCode(
        file_path=file_path,
        language=language,
    )