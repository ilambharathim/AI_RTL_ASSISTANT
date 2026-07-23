from fastapi import APIRouter, UploadFile, File

from app.schemas.upload_response import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_files(
    specification: UploadFile = File(...),
    rtl: UploadFile = File(...),
    testbench: UploadFile = File(...),
):
    """
    Upload Specification, RTL and Testbench.
    """

    return UploadService.upload_files(
        specification,
        rtl,
        testbench,
    )