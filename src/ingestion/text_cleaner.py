"""
src/ingestion/text_cleaner.py
Single Responsibility: Clean and normalize raw text extracted from academic PDFs.
"""
import re


class TextCleaner:
    """Stateless utility for normalizing PDF layout and formatting noise."""

    @staticmethod
    def clean(raw_text: str) -> str:
        """
        Applies sequential regex passes to repair broken hyphenation,
        unwrap artificial column line-breaks, and strip control characters.
        """
        if not raw_text:
            return ""

        # 1. Rejoin words hyphenated across line wraps (e.g., "trans-\nformer" -> "transformer")
        text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", raw_text)

        # 2. Replace single newlines inside paragraphs with spaces while keeping paragraph breaks (\n\n)
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        # 3. Strip non-printable ASCII control bytes common in LaTeX math fonts
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        # 4. Collapse multiple spaces/tabs into a single space
        text = re.sub(r"\s+", " ", text)

        return text.strip()