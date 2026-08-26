"""
SpecificationReader robustness tests covering missing branches.
"""

import pytest
from pathlib import Path
from app.parsers.specification.reader import SpecificationReader
from app.parsers.specification.exceptions import (
    SpecificationReadError,
    UnsupportedSpecificationFormatError,
)


def test_specification_reader_file_not_exists(tmp_path):
    """Line 82: file does not exist -> SpecificationReadError."""
    missing = tmp_path / "missing.txt"
    with pytest.raises(SpecificationReadError, match="does not exist"):
        SpecificationReader.read(missing)


def test_specification_reader_path_is_directory(tmp_path):
    """Line 143-144: path is a directory not a file -> SpecificationReadError."""
    with pytest.raises(SpecificationReadError, match="not a file"):
        SpecificationReader.read(tmp_path)


def test_specification_reader_unsupported_format(tmp_path):
    """Line 157, 163, 166: unsupported extension -> UnsupportedSpecificationFormatError."""
    pdf_file = tmp_path / "spec.pdf"
    pdf_file.write_text("dummy")
    with pytest.raises(UnsupportedSpecificationFormatError, match="Unsupported"):
        SpecificationReader.read(pdf_file)


def test_specification_reader_reads_valid_txt_file(tmp_path):
    """Line 159->162: valid .txt file is read successfully."""
    txt_file = tmp_path / "spec.txt"
    txt_file.write_text("# Requirements\n- REQ-1: Do something", encoding="utf-8")
    content = SpecificationReader.read(txt_file)
    assert "REQ-1" in content


def test_specification_reader_register_backend_duplicate_raises():
    """Line 82 register_backend: duplicate extension raises ValueError."""
    with pytest.raises(ValueError, match="already registered"):
        SpecificationReader.register_backend(".txt", None, replace=False)


def test_specification_reader_register_backend_replace_succeeds():
    """register_backend with replace=True works."""
    class DummyBackend:
        def read(self, path): return "dummy"

    original = SpecificationReader._backends[".txt"]
    try:
        SpecificationReader.register_backend(".txt", DummyBackend(), replace=True)
        txt_path = Path("/dev/null")
    finally:
        # Restore original backend
        SpecificationReader._backends[".txt"] = original
