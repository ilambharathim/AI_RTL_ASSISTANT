from fastapi import UploadFile

from app.schemas.upload_response import UploadResponse
from app.services.file_validator import FileValidator
from app.storage.file_storage import FileStorage


class UploadService:
    """
    Handles the complete upload workflow.
    """

    @staticmethod
    def upload_files(
        specification: UploadFile,
        rtl: UploadFile,
        testbench: UploadFile,
    ) -> UploadResponse:

        # Validate files
        FileValidator.validate(specification, "specification")
        FileValidator.validate(rtl, "rtl")
        FileValidator.validate(testbench, "testbench")

        # Save files
        spec_path = FileStorage.save_file(specification, "specification")
        rtl_path = FileStorage.save_file(rtl, "rtl")
        tb_path = FileStorage.save_file(testbench, "testbench")

        # Return response
        return UploadResponse(
            status="success",
            message="Files uploaded successfully.",
            specification=spec_path,
            rtl=rtl_path,
            testbench=tb_path,
        )