"""
Document Normalizer

Responsible for converting raw specification text into a
consistent format before lexical analysis.

The lexer should never need to deal with formatting issues.
"""

import re
import unicodedata


class DocumentNormalizer:

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize specification text.
        """

        # -----------------------------
        # Unicode normalization
        # -----------------------------
        text = unicodedata.normalize("NFKC", text)

        # -----------------------------
        # Normalize line endings
        # -----------------------------
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # -----------------------------
        # Replace tabs with spaces
        # -----------------------------
        text = text.replace("\t", "    ")

        # -----------------------------
        # Remove trailing spaces
        # -----------------------------
        text = "\n".join(line.rstrip() for line in text.split("\n"))

        # -----------------------------
        # Collapse multiple blank lines
        # -----------------------------
        text = re.sub(r"\n{3,}", "\n\n", text)

        # -----------------------------
        # Strip leading/trailing whitespace
        # -----------------------------
        text = text.strip()

        return text
