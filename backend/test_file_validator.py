"""
Unit tests for the RIVA upload file validator.
"""

from io import BytesIO

from fastapi import UploadFile

from app.infrastructure.uploads.file_validator import (
    FileValidator,
    UploadValidationError,
)


def create_upload(filename: str) -> UploadFile:
    """
    Create an in-memory uploaded file for testing.
    """

    return UploadFile(
        filename=filename,
        file=BytesIO(b"test content"),
    )


def test_valid_specification_file() -> None:
    file = create_upload("requirements.txt")

    FileValidator.validate(file, "specification")


def test_valid_rtl_file() -> None:
    file = create_upload("design.sv")

    FileValidator.validate(file, "rtl")


def test_valid_testbench_file() -> None:
    file = create_upload("testbench.v")

    FileValidator.validate(file, "testbench")


def test_extension_is_case_insensitive() -> None:
    file = create_upload("DESIGN.SV")

    FileValidator.validate(file, "rtl")


def test_invalid_extension() -> None:
    file = create_upload("design.cpp")

    try:
        FileValidator.validate(file, "rtl")
    except UploadValidationError as error:
        assert "Invalid rtl file type" in str(error)
    else:
        raise AssertionError(
            "Expected UploadValidationError for invalid extension."
        )


def test_directory_path_is_rejected() -> None:
    file = create_upload("../design.sv")

    try:
        FileValidator.validate(file, "rtl")
    except UploadValidationError as error:
        assert "must not contain directory paths" in str(error)
    else:
        raise AssertionError(
            "Expected UploadValidationError for directory path."
        )


def test_unknown_category() -> None:
    file = create_upload("design.sv")

    try:
        FileValidator.validate(file, "unknown")
    except UploadValidationError as error:
        assert "Unknown upload category" in str(error)
    else:
        raise AssertionError(
            "Expected UploadValidationError for unknown category."
        )


def main() -> None:
    tests = (
        test_valid_specification_file,
        test_valid_rtl_file,
        test_valid_testbench_file,
        test_extension_is_case_insensitive,
        test_invalid_extension,
        test_directory_path_is_rejected,
        test_unknown_category,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nFileValidator tests passed.")


if __name__ == "__main__":
    main()
