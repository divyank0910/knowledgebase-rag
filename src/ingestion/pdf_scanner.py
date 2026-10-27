"""
src/ingestion/pdf_scanner.py
"""
from pathlib import Path
from typing import List, Dict, Any
import pymupdf

from config.settings import PDF_SOURCE_DIR, KNOWN_PAPER_SIGNATURES
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LocalPDFScanner:
    """Scans a local directory for PDF files and resolves their metadata."""

    def __init__(self, pdf_dir: Path = PDF_SOURCE_DIR):
        self.pdf_dir = pdf_dir
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _validate_pdf_file(file_path: Path) -> None:
        """Verifies the file is non-empty and starts with the %PDF magic header."""
        if file_path.stat().st_size < 1024:
            raise ValueError(f"File '{file_path.name}' is empty or too small (<1 KB).")
        with open(file_path, "rb") as f:
            header = f.read(4)
        if header != b"%PDF":
            raise ValueError(f"File '{file_path.name}' does not have a valid %PDF header.")

    @staticmethod
    def _resolve_identity(file_path: Path) -> Dict[str, str]:
        """
        Determines a clean doc_id and title regardless of how the user named the file.
        Checks filename and Page 1 text against known papers, falling back to PDF metadata or filename.
        """
        with pymupdf.open(file_path) as doc:
            first_page_text = doc[0].get_text("text").lower() if len(doc) > 0 else ""
            pdf_meta_title = (doc.metadata or {}).get("title", "").strip()

        filename_lower = file_path.stem.lower()

        # 1. Match against the 5 known assignment papers by filename or Page 1 title text
        for sig in KNOWN_PAPER_SIGNATURES:
            if sig["doc_id"] in filename_lower or sig["keyword"] in first_page_text:
                return {"doc_id": sig["doc_id"], "title": sig["title"]}

        # 2. Fallback for any custom PDF placed in data/pdfs/
        resolved_title = pdf_meta_title if len(pdf_meta_title) > 4 else file_path.stem.replace("_", " ").title()
        return {"doc_id": file_path.stem, "title": resolved_title}

    def scan_directory(self) -> List[Dict[str, Any]]:
        """Scans data/pdfs/ and returns validated metadata records for all PDFs found."""
        pdf_files = sorted(self.pdf_dir.glob("*.pdf"))
        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found in '{self.pdf_dir}'. "
                f"Please place your downloaded PDF files into '{self.pdf_dir}' and re-run."
            )

        discovered_docs: List[Dict[str, Any]] = []
        for file_path in pdf_files:
            self._validate_pdf_file(file_path)
            identity = self._resolve_identity(file_path)
            record = {
                "doc_id": identity["doc_id"],
                "title": identity["title"],
                "file_name": file_path.name,
                "file_path": file_path,
                "size_kb": file_path.stat().st_size // 1024,
            }
            discovered_docs.append(record)
            logger.info(
                f"Discovered: '{file_path.name}' ({record['size_kb']} KB) -> "
                f"ID: [{record['doc_id']}] | Title: '{record['title']}'"
            )

        return discovered_docs