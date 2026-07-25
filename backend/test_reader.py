"""
Unit tests for the RIVA specification document reader.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from app.parsers.specification.exceptions import (
    SpecificationReadError,
    UnsupportedSpecificationFormatError,
)
from app.parsers.specification.reader import SpecificationReader


class StaticReaderBackend:
    """
    Test backend that returns predefined text.
    """

    def __init__(self, content: str) -> None:
        self.content = content

    def read(self, source_path: Path) -> str:
        assert source_path.exists()
        return self.content


def test_read_utf8_text_file() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "specification.txt"
        expected_content = "Module Name: design\nInputs:\nclk\n"

        source_path.write_text(
            expected_content,
            encoding="utf-8",
        )

        content = SpecificationReader.read(source_path)

        assert content == expected_content


def test_utf8_byte_order_mark_is_removed() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "specification.txt"
        expected_content = "Project Name: RIVA"

        source_path.write_text(
            expected_content,
            encoding="utf-8-sig",
        )

        content = SpecificationReader.read(source_path)

        assert content == expected_content
        assert not content.startswith("\ufeff")


def test_extension_matching_is_case_insensitive() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "SPECIFICATION.TXT"
        expected_content = "Module Name: uppercase_extension"

        source_path.write_text(
            expected_content,
            encoding="utf-8",
        )

        content = SpecificationReader.read(source_path)

        assert content == expected_content


def test_missing_file_is_rejected() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "missing.txt"

        try:
            SpecificationReader.read(source_path)

        except SpecificationReadError as error:
            assert "does not exist" in str(error)

        else:
            raise AssertionError(
                "Expected SpecificationReadError for a missing file."
            )


def test_directory_path_is_rejected() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory)

        try:
            SpecificationReader.read(source_path)

        except SpecificationReadError as error:
            assert "is not a file" in str(error)

        else:
            raise AssertionError(
                "Expected SpecificationReadError for a directory path."
            )


def test_unsupported_format_is_rejected() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "specification.pdf"

        source_path.write_bytes(b"not a real PDF")

        try:
            SpecificationReader.read(source_path)

        except UnsupportedSpecificationFormatError as error:
            assert "Unsupported specification format" in str(error)
            assert ".pdf" in str(error)

        else:
            raise AssertionError(
                "Expected UnsupportedSpecificationFormatError."
            )


def test_invalid_utf8_is_rejected() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "invalid.txt"

        source_path.write_bytes(b"\xff\xfe\x00\x80")

        try:
            SpecificationReader.read(source_path)

        except SpecificationReadError as error:
            assert "not valid UTF-8 text" in str(error)

        else:
            raise AssertionError(
                "Expected SpecificationReadError for invalid UTF-8."
            )


def test_custom_backend_registration() -> None:
    with TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "specification.mock"
        source_path.write_text(
            "raw mock data",
            encoding="utf-8",
        )

        original_backends = dict(SpecificationReader._backends)

        try:
            SpecificationReader.register_backend(
                "mock",
                StaticReaderBackend("Extracted mock specification"),
            )

            content = SpecificationReader.read(source_path)

            assert content == "Extracted mock specification"

        finally:
            SpecificationReader._backends = original_backends


def main() -> None:
    tests = (
        test_read_utf8_text_file,
        test_utf8_byte_order_mark_is_removed,
        test_extension_matching_is_case_insensitive,
        test_missing_file_is_rejected,
        test_directory_path_is_rejected,
        test_unsupported_format_is_rejected,
        test_invalid_utf8_is_rejected,
        test_custom_backend_registration,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecificationReader tests passed.")


if __name__ == "__main__":
    main()
