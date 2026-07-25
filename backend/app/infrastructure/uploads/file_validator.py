"""
Validation policies for files uploaded to RIVA.
"""

from pathlib import Path
from typing import ClassVar

from fastapi import UploadFile


class UploadValidationError(ValueError):
    """
    Raised when an uploaded file violates RIVA's upload policy.
    """


class FileValidator:
    """
    Validates uploaded files before they reach persistent storage.

    The validation policy is centralized here so API routes and storage
    adapters do not duplicate file-category rules.
    """

    ALLOWED_EXTENSIONS: ClassVar[dict[str, frozenset[str]]] = {
        "specification": frozenset({".pdf", ".docx", ".txt"}),
        "rtl": frozenset({".sv", ".v"}),
        "testbench": frozenset({".sv", ".v"}),
    }

    @classmethod
    def validate(cls, file: UploadFile, category: str) -> None:
        """
        Validate an uploaded file for the specified category.

        Args:
            file: File supplied through the FastAPI upload endpoint.
            category: RIVA file category.

        Raises:
            UploadValidationError: If the category, filename, or extension
                is invalid.
        """

        if category not in cls.ALLOWED_EXTENSIONS:
            raise UploadValidationError(
                f"Unknown upload category: {category}"
            )

        filename = (file.filename or "").strip()

        if not filename:
            raise UploadValidationError("Filename cannot be empty.")

        if "\x00" in filename:
            raise UploadValidationError(
                "Filename contains an invalid null character."
            )

        normalized_filename = filename.replace("\\", "/")

        if "/" in normalized_filename:
            raise UploadValidationError(
                "Filename must not contain directory paths."
            )

        extension = Path(normalized_filename).suffix.lower()

        if not extension:
            raise UploadValidationError(
                f"Uploaded {category} file must have an extension."
            )

        allowed_extensions = cls.ALLOWED_EXTENSIONS[category]

        if extension not in allowed_extensions:
            allowed_text = ", ".join(sorted(allowed_extensions))

            raise UploadValidationError(
                f"Invalid {category} file type: {extension}. "
                f"Allowed extensions: {allowed_text}"
            )
