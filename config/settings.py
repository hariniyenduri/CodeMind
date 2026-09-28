from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================
# PROJECT ROOT
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(BASE_DIR / ".env")


# ==========================================
# DIRECTORIES
# ==========================================

DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"
EXTRACTED_DIR = DATA_DIR / "extracted"
CHROMA_DIR = DATA_DIR / "chroma"


# Create directories automatically
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# LLM API KEYS
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# ==========================================
# EMBEDDING MODEL
# ==========================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ==========================================
# RAG CONFIGURATION
# ==========================================

TOP_K_RESULTS = 5

CHUNK_SIZE = 1200

CHUNK_OVERLAP = 200


# ==========================================
# SUPPORTED SOURCE FILES
# ==========================================

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".kts",
    ".html",
    ".css",
    ".sql",
}
