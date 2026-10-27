"""
src/ingestion/chunker.py
Single Responsibility: Segment extracted page text into overlapping chunks and persist to JSON.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHUNK_SEPARATORS,
    PROCESSED_CHUNKS_PATH,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SemanticChunker:
    """Splits page text into overlapping semantic chunks fitted for embedding models."""

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        separators: List[str] = CHUNK_SEPARATORS,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len,
        )

    def create_chunks(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Splits a list of cleaned page records into chunk records with traceable IDs."""
        chunks: List[Dict[str, Any]] = []

        for page in pages:
            segments = self.splitter.split_text(page["text"])
            for idx, segment_text in enumerate(segments, start=1):
                chunks.append({
                    "chunk_id": f"{page['doc_id']}_p{page['page_number']}_c{idx}",
                    "doc_id": page["doc_id"],
                    "paper_title": page["paper_title"],
                    "file_name": page["file_name"],
                    "page_number": page["page_number"],
                    "char_length": len(segment_text),
                    "text": segment_text,
                })

        logger.info(f"Segmented {len(pages)} pages into {len(chunks)} overlapping chunks.")
        return chunks

    @staticmethod
    def save_to_json(chunks: List[Dict[str, Any]], output_path: Path = PROCESSED_CHUNKS_PATH) -> Path:
        """Saves chunk records to data/processed/chunks.json."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(chunks)} chunks to '{output_path}'")
        return output_path

    @staticmethod
    def load_from_json(input_path: Path = PROCESSED_CHUNKS_PATH) -> List[Dict[str, Any]]:
        """Loads processed chunks from JSON for Task 2 vector indexing."""
        if not input_path.exists():
            raise FileNotFoundError(
                f"Chunks file not found at '{input_path}'. Run scripts/run_task1_ingestion.py first."
            )
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)