from pydantic import BaseModel


class UploadResponse(BaseModel):
    """
    Response returned after a successful upload.
    """

    status: str
    message: str
    specification: str
    rtl: str
    testbench: str