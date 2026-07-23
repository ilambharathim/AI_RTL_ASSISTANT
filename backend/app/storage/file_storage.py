from pathlib import Path
import shutil
from fastapi import UploadFile


class FileStorage:
    """
    Handles storing uploaded files in the appropriate directories.
    """

    BASE_UPLOAD_DIR = Path("uploads")

    DIRECTORIES = {
        "specification": BASE_UPLOAD_DIR / "specifications",
        "rtl": BASE_UPLOAD_DIR / "rtl",
        "testbench": BASE_UPLOAD_DIR / "testbench",
    }

    @classmethod
    def save_file(cls, file: UploadFile, category: str) -> str:
        """
        Save an uploaded file to the specified category folder.
        """

        if category not in cls.DIRECTORIES:
            raise ValueError(f"Unknown category: {category}")

        destination = cls.DIRECTORIES[category] / file.filename

        destination.parent.mkdir(parents=True, exist_ok=True)

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(destination)