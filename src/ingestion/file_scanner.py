from pathlib import Path

from config.settings import SUPPORTED_EXTENSIONS


# ==========================================
# DIRECTORIES TO IGNORE
# ==========================================

IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "bower_components",
    "vendor",
    "build",
    "dist",
    "target",
    "out",
    "coverage",
}


# ==========================================
# FILES TO IGNORE
# ==========================================

IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
}


# ==========================================
# SCAN PROJECT
# ==========================================

def scan_project(project_path: Path) -> list[Path]:
    """
    Scan an extracted project and return supported source files.

    Args:
        project_path: Root directory of the extracted project.

    Returns:
        List of supported source-code file paths.
    """

    project_path = Path(project_path)

    if not project_path.exists():
        raise FileNotFoundError(
            f"Project directory does not exist: {project_path}"
        )

    if not project_path.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {project_path}"
        )

    source_files = []

    for path in project_path.rglob("*"):

        # Ignore directories
        if path.is_dir():
            continue

        # Ignore unwanted files
        if path.name in IGNORED_FILES:
            continue

        # Ignore files inside unwanted directories
        if any(
            directory in IGNORED_DIRECTORIES
            for directory in path.parts
        ):
            continue

        # Check extension
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            source_files.append(path)

    return sorted(source_files)