"""
RIVA project upload API route.
"""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.infrastructure.uploads.file_validator import UploadValidationError
from app.infrastructure.uploads.upload_service import UploadService
from app.schemas.upload_response import UploadResponse


router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
def upload_files(
    specification: UploadFile = File(...),
    rtl: UploadFile = File(...),
    testbench: UploadFile = File(...),
) -> UploadResponse:
    """
    Validate and store a specification, RTL source, and testbench.

    This endpoint uses a synchronous function because file storage performs
    blocking filesystem operations. FastAPI executes synchronous route
    functions in its worker thread pool.
    """

    try:
        result = UploadService.upload_files(
            specification=specification,
            rtl=rtl,
            testbench=testbench,
        )

    except UploadValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store the uploaded project files.",
        ) from error

    return UploadResponse(
        status="success",
        message="Files uploaded successfully.",
        specification=result.specification,
        rtl=result.rtl,
        testbench=result.testbench,
    )
