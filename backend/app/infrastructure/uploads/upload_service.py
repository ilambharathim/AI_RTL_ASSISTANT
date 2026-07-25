"""
Upload workflow for RIVA project artifacts.
"""

from contextlib import suppress
from dataclasses import dataclass

from fastapi import UploadFile

from app.infrastructure.uploads.file_validator import FileValidator
from app.storage.file_storage import FileStorage


@dataclass(frozen=True, slots=True)
class UploadResult:
    """
    Paths produced by a successful project upload.
    """

    specification: str
    rtl: str
    testbench: str


class UploadService:
    """
    Coordinates validation and storage of uploaded RIVA project files.

    All files are validated before storage begins. If storage fails after
    one or more files have already been written, those files are deleted
    as a best-effort rollback.
    """

    @classmethod
    def upload_files(
        cls,
        specification: UploadFile,
        rtl: UploadFile,
        testbench: UploadFile,
    ) -> UploadResult:
        """
        Validate and store specification, RTL, and testbench files.

        Args:
            specification: Uploaded requirements specification.
            rtl: Uploaded RTL source file.
            testbench: Uploaded testbench source file.

        Returns:
            UploadResult containing the three stored file paths.

        Raises:
            UploadValidationError: If any uploaded file is invalid.
            OSError: If one of the files cannot be stored.
        """

        uploads = (
            ("specification", specification),
            ("rtl", rtl),
            ("testbench", testbench),
        )

        for category, uploaded_file in uploads:
            FileValidator.validate(
                uploaded_file,
                category,
            )

        stored_paths: list[str] = []

        try:
            specification_path = FileStorage.save_file(
                specification,
                "specification",
            )
            stored_paths.append(specification_path)

            rtl_path = FileStorage.save_file(
                rtl,
                "rtl",
            )
            stored_paths.append(rtl_path)

            testbench_path = FileStorage.save_file(
                testbench,
                "testbench",
            )
            stored_paths.append(testbench_path)

        except Exception:
            for stored_path in reversed(stored_paths):
                with suppress(OSError, ValueError):
                    FileStorage.delete_file(stored_path)

            raise

        return UploadResult(
            specification=specification_path,
            rtl=rtl_path,
            testbench=testbench_path,
        )
