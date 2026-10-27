"""
config/settings.py
"""
from pathlib import Path
from typing import List, Dict

# 1. Base Directory Paths
ROOT_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = ROOT_DIR / "data"
PDF_SOURCE_DIR: Path = DATA_DIR / "pdfs"
PROCESSED_CHUNKS_PATH: Path = DATA_DIR / "processed" / "chunks.json"

VECTORSTORE_DIR: Path = ROOT_DIR / "vectorstore"
FAISS_INDEX_PATH: Path = VECTORSTORE_DIR / "faiss_index"

OUTPUTS_DIR: Path = ROOT_DIR / "outputs"
EVALUATION_CSV_PATH: Path = OUTPUTS_DIR / "evaluation_results.csv"
EVALUATION_MD_PATH: Path = OUTPUTS_DIR / "evaluation_summary.md"

# 2.(Allows you to name PDFs anything you want in data/pdfs/)
KNOWN_PAPER_SIGNATURES: List[Dict[str, str]] = [
    {
        "doc_id": "1706.03762",
        "title": "Attention Is All You Need (Transformer)",
        "keyword": "attention is all you need",
    },
    {
        "doc_id": "1810.04805",
        "title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "keyword": "pre-training of deep bidirectional transformers",
    },
    {
        "doc_id": "2005.14165",
        "title": "Language Models are Few-Shot Learners (GPT-3)",
        "keyword": "language models are few-shot learners",
    },
    {
        "doc_id": "1907.11692",
        "title": "RoBERTa: A Robustly Optimized BERT Pretraining Approach",
        "keyword": "robustly optimized bert pretraining approach",
    },
    {
        "doc_id": "1910.10683",
        "title": "Exploring the Limits of Transfer Learning with T5",
        "keyword": "exploring the limits of transfer learning with a unified text-to-text",
    },
]

# 3. Task 1: Extraction & Chunking Parameters
MIN_PAGE_CHAR_LENGTH: int = 50
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 150
CHUNK_SEPARATORS: List[str] = ["\n\n", "\n", ". ", " ", ""]

# 4. Task 2: Embedding & FAISS Settings
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_RETRIEVAL: int = 4

# 5. Task 3 & 4: LLM & Memory Settings
OLLAMA_BASE_URL: str = "http://localhost:11434"
OLLAMA_MODEL_NAME: str = "llama3.2"
HF_FALLBACK_MODEL: str = "google/flan-t5-base"
LLM_TEMPERATURE: float = 0.0
MEMORY_WINDOW_SIZE: int = 4