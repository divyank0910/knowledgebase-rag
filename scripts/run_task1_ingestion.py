"""
scripts/run_task1_ingestion.py
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingestion.pdf_scanner import LocalPDFScanner
from src.ingestion.pdf_extractor import PDFExtractor
from src.ingestion.chunker import SemanticChunker


def main() -> None:
    print("=" * 75)
    print("TASK 1: LOCAL PDF INGESTION, CLEANING & SEMANTIC CHUNKING")
    print("=" * 75)

    # 1. Scan data/pdfs/ for user-placed PDF files
    scanner = LocalPDFScanner()
    discovered_pdfs = scanner.scan_directory()

    # 2. Extract and clean text page-by-page
    extractor = PDFExtractor()
    extracted_pages = extractor.extract_all(discovered_pdfs)

    # 3. Chunk pages and persist to data/processed/chunks.json
    chunker = SemanticChunker()
    chunks = chunker.create_chunks(extracted_pages)
    saved_path = chunker.save_to_json(chunks)

    # 4. Display summary table
    paper_counts = Counter((c["file_name"], c["paper_title"]) for c in chunks)
    print("\n--- Task 1 Ingestion Summary ---")
    print(f"{'File Name':<22} | {'Resolved Title':<42} | {'Chunks':>6}")
    print("-" * 75)
    for (fname, title), count in paper_counts.items():
        print(f"{fname[:22]:<22} | {title[:42]:<42} | {count:6d}")
    print("-" * 75)
    print(f"Total Chunks Saved : {len(chunks)}")
    print(f"Output JSON Path   : {saved_path}")
    print("=" * 75)


if __name__ == "__main__":
    main()