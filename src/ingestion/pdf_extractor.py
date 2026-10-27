"""
src/ingestion/pdf_extractor.py
Single Responsibility: Extract page-level text from PDF files using PyMuPDF.
"""
from typing import List, Dict, Any
import pymupdf

from config.settings import MIN_PAGE_CHAR_LENGTH
from src.ingestion.text_cleaner import TextCleaner
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PDFExtractor:
    """Extracts cleaned page-by-page text from discovered PDF records."""

    def __init__(self, min_page_chars: int = MIN_PAGE_CHAR_LENGTH):
        self.min_page_chars = min_page_chars
        self.cleaner = TextCleaner()

    def extract_single_pdf(self, doc_record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extracts all valid text pages from a single PDF document."""
        pages_output: List[Dict[str, Any]] = []
        pdf_path = doc_record["file_path"]

        with pymupdf.open(pdf_path) as pdf_doc:
            total_pages = len(pdf_doc)
            for page_idx in range(total_pages):
                raw_text = pdf_doc[page_idx].get_text("text")
                cleaned_text = self.cleaner.clean(raw_text)

                if len(cleaned_text) < self.min_page_chars:
                    continue

                pages_output.append({
                    "doc_id": doc_record["doc_id"],
                    "paper_title": doc_record["title"],
                    "file_name": doc_record["file_name"],
                    "page_number": page_idx + 1,
                    "total_pages": total_pages,
                    "text": cleaned_text,
                })

        logger.info(
            f"Extracted {len(pages_output)}/{total_pages} valid pages from '{doc_record['file_name']}'"
        )
        return pages_output

    def extract_all(self, doc_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extracts cleaned pages across all discovered PDF documents."""
        all_pages: List[Dict[str, Any]] = []
        for record in doc_records:
            all_pages.extend(self.extract_single_pdf(record))
        return all_pages