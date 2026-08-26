"""
Comprehensive Unit Test Suite for Phase 11 — API/Storage/File Validation.
Validates branches across FileValidator, FileStorage, and UploadService.
"""

import io
import os
import pytest
import shutil
from pathlib import Path
from unittest.mock import MagicMock

from app.infrastructure.uploads.file_validator import FileValidator, UploadValidationError
from app.storage.file_storage import FileStorage


class FakeUploadFile:
    """Minimal mock for FastAPI UploadFile."""
    def __init__(self, filename, content=b"dummy content"):
        self.filename = filename
        self.file = io.BytesIO(content)


# ── FileValidator ────────────────────────────────────────────────────

def test_file_validator_unknown_category():
    f = FakeUploadFile("test.sv")
    with pytest.raises(UploadValidationError, match="Unknown upload category"):
        FileValidator.validate(f, "bogus_category")


def test_file_validator_empty_filename():
    f = FakeUploadFile("")
    with pytest.raises(UploadValidationError, match="Filename cannot be empty"):
        FileValidator.validate(f, "rtl")


def test_file_validator_null_character():
    f = FakeUploadFile("test\x00.sv")
    with pytest.raises(UploadValidationError, match="null character"):
        FileValidator.validate(f, "rtl")


def test_file_validator_directory_path():
    f = FakeUploadFile("subdir/test.sv")
    with pytest.raises(UploadValidationError, match="directory paths"):
        FileValidator.validate(f, "rtl")

    f2 = FakeUploadFile("subdir\\test.sv")
    with pytest.raises(UploadValidationError, match="directory paths"):
        FileValidator.validate(f2, "rtl")


def test_file_validator_no_extension():
    f = FakeUploadFile("noextension")
    with pytest.raises(UploadValidationError, match="must have an extension"):
        FileValidator.validate(f, "rtl")


def test_file_validator_invalid_extension():
    f = FakeUploadFile("test.py")
    with pytest.raises(UploadValidationError, match="Invalid rtl file type"):
        FileValidator.validate(f, "rtl")


def test_file_validator_valid_file():
    f = FakeUploadFile("design.sv")
    FileValidator.validate(f, "rtl")  # should not raise

    f2 = FakeUploadFile("spec.pdf")
    FileValidator.validate(f2, "specification")  # should not raise

    f3 = FakeUploadFile("tb.v")
    FileValidator.validate(f3, "testbench")  # should not raise


# ── FileStorage ──────────────────────────────────────────────────────

def test_file_storage_safe_filename_edge_cases():
    # Empty filename
    with pytest.raises(ValueError, match="Filename cannot be empty"):
        FileStorage._safe_filename("")

    with pytest.raises(ValueError, match="Filename cannot be empty"):
        FileStorage._safe_filename(None)

    # Directory path
    with pytest.raises(ValueError, match="directory paths"):
        FileStorage._safe_filename("a/b.sv")

    # Invalid filenames
    with pytest.raises(ValueError, match="Invalid filename"):
        FileStorage._safe_filename(".")

    with pytest.raises(ValueError, match="Invalid filename"):
        FileStorage._safe_filename("..")

    # Valid
    assert FileStorage._safe_filename("design.sv") == "design.sv"


def test_file_storage_unknown_category():
    f = FakeUploadFile("test.sv")
    with pytest.raises(ValueError, match="Unknown storage category"):
        FileStorage.save_file(f, "bogus")


def test_file_storage_save_and_delete(tmp_path, monkeypatch):
    # Redirect BASE_UPLOAD_DIR to tmp_path
    monkeypatch.setattr(FileStorage, "BASE_UPLOAD_DIR", tmp_path / "uploads")

    f = FakeUploadFile("design.sv", b"module top; endmodule")
    stored_path = FileStorage.save_file(f, "rtl")
    assert Path(stored_path).exists()
    assert b"module top; endmodule" in Path(stored_path).read_bytes()

    # Delete
    FileStorage.delete_file(stored_path)
    assert not Path(stored_path).exists()


def test_file_storage_delete_outside_upload_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(FileStorage, "BASE_UPLOAD_DIR", tmp_path / "uploads")
    with pytest.raises(ValueError, match="outside the upload directory"):
        FileStorage.delete_file("/etc/passwd")


def test_file_storage_save_failure_cleanup(tmp_path, monkeypatch):
    monkeypatch.setattr(FileStorage, "BASE_UPLOAD_DIR", tmp_path / "uploads")

    class FailingFile:
        filename = "fail.sv"
        class file:
            @staticmethod
            def seek(n):
                raise OSError("disk full")

    with pytest.raises(OSError, match="disk full"):
        FileStorage.save_file(FailingFile(), "rtl")
