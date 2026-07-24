from pathlib import Path


class SpecificationReader:
    """
    Reads a specification file and returns its text content.
    """

    def read(self, file_path: str) -> str:
        """
        Read specification file.

        Args:
            file_path: Path to specification file

        Returns:
            File content as string
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Specification file not found: {file_path}"
            )

        return path.read_text(encoding="utf-8")