"""
Unit tests for the RIVA upload workflow.
"""

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import call, patch

from fastapi import UploadFile

from app.infrastructure.uploads.file_validator import UploadValidationError
from app.infrastructure.uploads.upload_service import UploadService
from app.storage.file_storage import FileStorage


def create_upload(
    filename: str,
    content: bytes = b"RIVA test content",
) -> UploadFile:
    """
    Create an in-memory uploaded file for testing.
    """

    return UploadFile(
        filename=filename,
        file=BytesIO(content),
    )


def test_successful_upload() -> None:
    """
    Verify that all three valid project files are stored.
    """

    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR

        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        try:
            specification = create_upload(
                "requirements.txt",
                b"Module Name: design",
            )

            rtl = create_upload(
                "design.sv",
                b"module design; endmodule",
            )

            testbench = create_upload(
                "design_tb.sv",
                b"module design_tb; endmodule",
            )

            result = UploadService.upload_files(
                specification=specification,
                rtl=rtl,
                testbench=testbench,
            )

            specification_path = Path(result.specification)
            rtl_path = Path(result.rtl)
            testbench_path = Path(result.testbench)

            assert specification_path.exists()
            assert rtl_path.exists()
            assert testbench_path.exists()

            assert specification_path.read_bytes() == (
                b"Module Name: design"
            )

            assert rtl_path.read_bytes() == (
                b"module design; endmodule"
            )

            assert testbench_path.read_bytes() == (
                b"module design_tb; endmodule"
            )

        finally:
            FileStorage.BASE_UPLOAD_DIR = original_upload_directory


def test_invalid_file_is_rejected_before_storage() -> None:
    """
    Verify validation completes before any file is stored.
    """

    specification = create_upload("requirements.txt")
    rtl = create_upload("design.cpp")
    testbench = create_upload("design_tb.sv")

    with patch.object(FileStorage, "save_file") as save_file:
        try:
            UploadService.upload_files(
                specification=specification,
                rtl=rtl,
                testbench=testbench,
            )

        except UploadValidationError as error:
            assert "Invalid rtl file type" in str(error)

        else:
            raise AssertionError(
                "Expected UploadValidationError for invalid RTL."
            )

        save_file.assert_not_called()


def test_storage_failure_rolls_back_previous_files() -> None:
    """
    Verify earlier stored files are deleted when a later save fails.
    """

    specification = create_upload("requirements.txt")
    rtl = create_upload("design.sv")
    testbench = create_upload("design_tb.sv")

    specification_path = "uploads/specifications/specification.txt"
    rtl_path = "uploads/rtl/design.sv"

    with patch.object(
        FileStorage,
        "save_file",
        side_effect=[
            specification_path,
            rtl_path,
            OSError("Simulated storage failure"),
        ],
    ), patch.object(
        FileStorage,
        "delete_file",
    ) as delete_file:
        try:
            UploadService.upload_files(
                specification=specification,
                rtl=rtl,
                testbench=testbench,
            )

        except OSError as error:
            assert "Simulated storage failure" in str(error)

        else:
            raise AssertionError(
                "Expected OSError from simulated storage failure."
            )

        assert delete_file.call_args_list == [
            call(rtl_path),
            call(specification_path),
        ]


def main() -> None:
    tests = (
        test_successful_upload,
        test_invalid_file_is_rejected_before_storage,
        test_storage_failure_rolls_back_previous_files,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nUploadService tests passed.")


if __name__ == "__main__":
    main()
