"""
Validate the RIVA SystemVerilog keyword database.
"""

import re
import sys

from app.language.systemverilog.ieee1800_2023_keywords import (
    IEEE1800_2023_RESERVED_KEYWORDS,
)


IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def main() -> int:
    keywords = sorted(IEEE1800_2023_RESERVED_KEYWORDS)

    print(f"Checking {len(keywords)} keywords...")

    previous = None

    for keyword in keywords:

        if keyword != keyword.strip():
            raise ValueError(f"Whitespace detected: {keyword!r}")

        if not keyword:
            raise ValueError("Empty keyword detected.")

        if not IDENTIFIER_PATTERN.fullmatch(keyword):
            raise ValueError(f"Invalid keyword: {keyword}")

        if previous == keyword:
            raise ValueError(f"Duplicate keyword: {keyword}")

        previous = keyword

    print("Keyword database validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
