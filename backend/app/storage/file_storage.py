"""
Persistent storage adapter for uploaded RIVA project files.
"""

import os
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class FileStorage:
    """
    Stores uploaded files in category-specific directories.

    Uploaded files are assigned unique stored filenames so that files with
    identical original names cannot overwrite one another.

    Files are first written to temporary paths and then atomically renamed
    after the write succeeds.
    """

    BASE_UPLOAD_DIR = Path("uploads")

    CATEGORY_DIRECTORIES = {
        "specification": "specifications",
        "rtl": "rtl",
        "testbench": "testbench",
    }

    @classmethod
    def save_file(cls, file: UploadFile, category: str) -> str:
        """
        Store an uploaded file and return its stored path.

        Args:
            file: File supplied through the FastAPI upload endpoint.
            category: RIVA upload category.

        Returns:
            The path of the stored file.

        Raises:
            ValueError: If the category or filename is invalid.
            OSError: If the file cannot be written.
        """

        if category not in cls.CATEGORY_DIRECTORIES:
            raise ValueError(f"Unknown storage category: {category}")

        safe_filename = cls._safe_filename(file.filename)

        destination_directory = (
            cls.BASE_UPLOAD_DIR
            / cls.CATEGORY_DIRECTORIES[category]
        )

        destination_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        stored_filename = f"{uuid4().hex}_{safe_filename}"
        destination = destination_directory / stored_filename
        temporary_path = destination_directory / (
            f".{stored_filename}.part"
        )

        try:
            file.file.seek(0)

            with temporary_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                buffer.flush()
                os.fsync(buffer.fileno())

            temporary_path.replace(destination)

        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise

        return str(destination)

    @classmethod
    def delete_file(cls, stored_path: str) -> None:
        """
        Delete a previously stored upload.

        Paths outside the configured upload directory are rejected.
        """

        upload_root = cls.BASE_UPLOAD_DIR.resolve()
        candidate = Path(stored_path).resolve()

        if not candidate.is_relative_to(upload_root):
            raise ValueError(
                "Refusing to delete a path outside the upload directory."
            )

        candidate.unlink(missing_ok=True)

    @staticmethod
    def _safe_filename(filename: str | None) -> str:
        """
        Validate a filename and reject directory components.
        """

        if not filename:
            raise ValueError("Filename cannot be empty.")

        normalized_filename = filename.strip().replace("\\", "/")

        if "/" in normalized_filename:
            raise ValueError(
                "Filename must not contain directory paths."
            )

        safe_filename = Path(normalized_filename).name

        if safe_filename in {"", ".", ".."}:
            raise ValueError("Invalid filename.")

        return safe_filename
