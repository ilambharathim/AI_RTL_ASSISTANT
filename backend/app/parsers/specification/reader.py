"""
Specification document reader for the RIVA compiler frontend.

The SpecificationReader dispatches documents to format-specific reader
backends. Plain UTF-8 text is supported initially. Additional readers for
PDF, DOCX, Markdown, HTML, and other formats can be registered later
without changing the compiler pipeline.
"""

from pathlib import Path
from typing import ClassVar, Protocol

from app.parsers.specification.exceptions import (
    SpecificationReadError,
    UnsupportedSpecificationFormatError,
)


class ReaderBackend(Protocol):
    """
    Interface implemented by format-specific document readers.
    """

    def read(self, source_path: Path) -> str:
        """
        Read a document and return its textual content.
        """


class Utf8TextReader:
    """
    Reads deterministic UTF-8 text documents.

    The ``utf-8-sig`` encoding accepts ordinary UTF-8 files and also removes
    an optional UTF-8 byte-order mark.
    """

    def read(self, source_path: Path) -> str:
        """
        Read a UTF-8 text document.
        """

        return source_path.read_text(encoding="utf-8-sig")


class SpecificationReader:
    """
    Reads specification documents through registered format backends.

    File-format dispatch is centralized here so downstream normalization,
    lexical analysis, parsing, and semantic analysis operate on text without
    depending on PDF, DOCX, or filesystem implementation details.
    """

    _backends: ClassVar[dict[str, ReaderBackend]] = {
        ".txt": Utf8TextReader(),
    }

    @classmethod
    def register_backend(
        cls,
        extension: str,
        backend: ReaderBackend,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register a reader backend for a file extension.

        Args:
            extension: Extension such as ``.txt`` or ``.pdf``.
            backend: Format-specific reader implementation.
            replace: Permit replacing an existing registration.

        Raises:
            ValueError: If the extension is invalid or already registered.
        """

        normalized_extension = cls._normalize_extension(extension)

        if normalized_extension in cls._backends and not replace:
            raise ValueError(
                "A specification reader is already registered for "
                f"{normalized_extension}."
            )

        cls._backends[normalized_extension] = backend

    @classmethod
    def read(cls, source: str | Path) -> str:
        """
        Read a specification document.

        Args:
            source: Path to the specification document.

        Returns:
            The extracted textual document content.

        Raises:
            SpecificationReadError: If the path is invalid, unreadable, or
                contains invalid UTF-8 data.
            UnsupportedSpecificationFormatError: If no backend is registered
                for the document extension.
        """

        source_path = Path(source).expanduser()

        if not source_path.exists():
            raise SpecificationReadError(
                f"Specification file does not exist: {source_path}"
            )

        if not source_path.is_file():
            raise SpecificationReadError(
                f"Specification path is not a file: {source_path}"
            )

        extension = source_path.suffix.lower()

        backend = cls._backends.get(extension)

        if backend is None:
            supported_extensions = ", ".join(
                sorted(cls._backends)
            )

            raise UnsupportedSpecificationFormatError(
                f"Unsupported specification format: "
                f"{extension or '<no extension>'}. "
                f"Supported formats: {supported_extensions}"
            )

        try:
            return backend.read(source_path)

        except UnicodeDecodeError as error:
            raise SpecificationReadError(
                f"Specification file is not valid UTF-8 text: "
                f"{source_path}"
            ) from error

        except OSError as error:
            raise SpecificationReadError(
                f"Unable to read specification file: {source_path}"
            ) from error

    @staticmethod
    def _normalize_extension(extension: str) -> str:
        """
        Normalize and validate a reader extension.
        """

        normalized_extension = extension.strip().lower()

        if not normalized_extension:
            raise ValueError("Reader extension cannot be empty.")

        if not normalized_extension.startswith("."):
            normalized_extension = f".{normalized_extension}"

        if normalized_extension == ".":
            raise ValueError("Reader extension cannot be only a dot.")

        if "/" in normalized_extension or "\\" in normalized_extension:
            raise ValueError(
                "Reader extension must not contain directory paths."
            )

        return normalized_extension
