"""Configuration with project-root-relative paths."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
KNOWLEDGE_DIR = ROOT / "knowledge_manual"
STORAGE_DIR = ROOT / "storage"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = max(1, min(8, int(os.getenv("TOP_K", "4"))))
MAX_HISTORY_MESSAGES = max(2, min(30, int(os.getenv("MAX_HISTORY_MESSAGES", "12"))))
