"""
Integration tests for the RIVA upload API endpoint.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from app.main import app
from app.storage.file_storage import FileStorage


client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to RIVA"
    }


def test_successful_upload_endpoint() -> None:
    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR

        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        try:
            response = client.post(
                "/upload",
                files={
                    "specification": (
                        "requirements.txt",
                        b"Module Name: design",
                        "text/plain",
                    ),
                    "rtl": (
                        "design.sv",
                        b"module design; endmodule",
                        "text/plain",
                    ),
                    "testbench": (
                        "design_tb.sv",
                        b"module design_tb; endmodule",
                        "text/plain",
                    ),
                },
            )

            assert response.status_code == 200

            payload = response.json()

            assert payload["status"] == "success"
            assert payload["message"] == (
                "Files uploaded successfully."
            )

            specification_path = Path(payload["specification"])
            rtl_path = Path(payload["rtl"])
            testbench_path = Path(payload["testbench"])

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


def test_invalid_rtl_extension_returns_400() -> None:
    with TemporaryDirectory() as temporary_directory:
        original_upload_directory = FileStorage.BASE_UPLOAD_DIR

        FileStorage.BASE_UPLOAD_DIR = (
            Path(temporary_directory) / "uploads"
        )

        try:
            response = client.post(
                "/upload",
                files={
                    "specification": (
                        "requirements.txt",
                        b"Module Name: design",
                        "text/plain",
                    ),
                    "rtl": (
                        "design.cpp",
                        b"invalid rtl",
                        "text/plain",
                    ),
                    "testbench": (
                        "design_tb.sv",
                        b"module design_tb; endmodule",
                        "text/plain",
                    ),
                },
            )

            assert response.status_code == 400

            payload = response.json()

            assert "Invalid rtl file type" in payload["detail"]

            upload_directory = FileStorage.BASE_UPLOAD_DIR

            assert not upload_directory.exists()

        finally:
            FileStorage.BASE_UPLOAD_DIR = original_upload_directory


def main() -> None:
    tests = (
        test_root_endpoint,
        test_successful_upload_endpoint,
        test_invalid_rtl_extension_returns_400,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nUpload API integration tests passed.")


if __name__ == "__main__":
    main()
