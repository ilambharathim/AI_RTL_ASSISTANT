"""
Unit tests for RIVA uploaded-file storage.
"""

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import UploadFile

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


def test_save_file() -> None:
    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR
        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        try:
            uploaded_file = create_upload(
                filename="design.sv",
                content=b"module design; endmodule",
            )

            stored_path = FileStorage.save_file(
                uploaded_file,
                "rtl",
            )

            stored_file = Path(stored_path)

            assert stored_file.exists()
            assert stored_file.parent.name == "rtl"
            assert stored_file.name.endswith("_design.sv")
            assert stored_file.read_bytes() == (
                b"module design; endmodule"
            )

        finally:
            FileStorage.BASE_UPLOAD_DIR = original_upload_directory


def test_duplicate_filenames_do_not_overwrite() -> None:
    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR
        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        try:
            first_upload = create_upload(
                filename="design.sv",
                content=b"first",
            )

            second_upload = create_upload(
                filename="design.sv",
                content=b"second",
            )

            first_path = FileStorage.save_file(
                first_upload,
                "rtl",
            )

            second_path = FileStorage.save_file(
                second_upload,
                "rtl",
            )

            assert first_path != second_path
            assert Path(first_path).read_bytes() == b"first"
            assert Path(second_path).read_bytes() == b"second"

        finally:
            FileStorage.BASE_UPLOAD_DIR = original_upload_directory


def test_delete_file() -> None:
    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR
        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        try:
            uploaded_file = create_upload("requirements.txt")

            stored_path = FileStorage.save_file(
                uploaded_file,
                "specification",
            )

            assert Path(stored_path).exists()

            FileStorage.delete_file(stored_path)

            assert not Path(stored_path).exists()

        finally:
            FileStorage.BASE_UPLOAD_DIR = original_upload_directory


def test_unknown_category_is_rejected() -> None:
    uploaded_file = create_upload("design.sv")

    try:
        FileStorage.save_file(
            uploaded_file,
            "unknown",
        )

    except ValueError as error:
        assert "Unknown storage category" in str(error)

    else:
        raise AssertionError(
            "Expected ValueError for an unknown storage category."
        )


def test_directory_filename_is_rejected() -> None:
    uploaded_file = create_upload("../design.sv")

    try:
        FileStorage.save_file(
            uploaded_file,
            "rtl",
        )

    except ValueError as error:
        assert "must not contain directory paths" in str(error)

    else:
        raise AssertionError(
            "Expected ValueError for a filename containing a path."
        )


def test_delete_outside_upload_directory_is_rejected() -> None:
    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR
        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        outside_file = Path(temporary_directory) / "outside.txt"
        outside_file.write_text(
            "must not be deleted",
            encoding="utf-8",
        )

        try:
            try:
                FileStorage.delete_file(str(outside_file))

            except ValueError as error:
                assert "outside the upload directory" in str(error)

            else:
                raise AssertionError(
                    "Expected ValueError for an outside path."
                )

            assert outside_file.exists()

        finally:
            FileStorage.BASE_UPLOAD_DIR = original_upload_directory


def main() -> None:
    tests = (
        test_save_file,
        test_duplicate_filenames_do_not_overwrite,
        test_delete_file,
        test_unknown_category_is_rejected,
        test_directory_filename_is_rejected,
        test_delete_outside_upload_directory_is_rejected,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nFileStorage tests passed.")


if __name__ == "__main__":
    main()
