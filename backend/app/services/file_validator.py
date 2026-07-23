from fastapi import HTTPException, UploadFile


class FileValidator:
    """
    Validates uploaded files before they are stored.
    """

    SPEC_EXTENSIONS = {".pdf", ".docx", ".txt"}
    RTL_EXTENSIONS = {".sv", ".v"}

    @staticmethod
    def validate(file: UploadFile, file_type: str) -> None:
        """
        Validate uploaded file based on its type.
        """

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename cannot be empty."
            )

        extension = "." + file.filename.split(".")[-1].lower()

        if file_type == "specification":
            allowed = FileValidator.SPEC_EXTENSIONS

        elif file_type in ("rtl", "testbench"):
            allowed = FileValidator.RTL_EXTENSIONS

        else:
            raise HTTPException(
                status_code=400,
                detail="Unknown file category."
            )

        if extension not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {file_type} file type: {extension}"
            )