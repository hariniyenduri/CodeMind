from pathlib import Path
from zipfile import ZipFile, BadZipFile

from config.settings import EXTRACTED_DIR


class ZipExtractionError(Exception):
    """Raised when a ZIP file cannot be safely extracted."""


def is_safe_path(base_dir: Path, target_path: Path) -> bool:
    """
    Check whether the target path stays inside the base directory.
    This prevents ZIP path traversal attacks.
    """

    try:
        target_path.resolve().relative_to(base_dir.resolve())
        return True
    except ValueError:
        return False


def extract_project(zip_path: Path) -> Path:
    """
    Safely extract a project ZIP file.

    Args:
        zip_path: Path to the uploaded ZIP file.

    Returns:
        Path to the extracted project directory.
    """

    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise ZipExtractionError("ZIP file does not exist.")

    if not zip_path.is_file():
        raise ZipExtractionError("The provided path is not a file.")

    if zip_path.suffix.lower() != ".zip":
        raise ZipExtractionError("Only ZIP files are supported.")

    project_name = zip_path.stem

    extraction_dir = EXTRACTED_DIR / project_name
    extraction_dir.mkdir(parents=True, exist_ok=True)

    try:
        with ZipFile(zip_path, "r") as zip_ref:

            for member in zip_ref.infolist():

                target_path = extraction_dir / member.filename

                if not is_safe_path(extraction_dir, target_path):
                    raise ZipExtractionError(
                        f"Unsafe path detected in ZIP: {member.filename}"
                    )

            for member in zip_ref.infolist():
                zip_ref.extract(member, extraction_dir)

    except BadZipFile as exc:
        raise ZipExtractionError(
            "The uploaded file is not a valid ZIP archive."
        ) from exc

    return extraction_dir