from app.language.systemverilog.ieee1800_2023_keywords import (
    IEEE1800_2023_RESERVED_KEYWORDS,
)

def test_keyword_database_exists():
    assert isinstance(
        IEEE1800_2023_RESERVED_KEYWORDS,
        frozenset,
    )

def test_keyword_database_unique():
    assert len(
        IEEE1800_2023_RESERVED_KEYWORDS
    ) == len(set(IEEE1800_2023_RESERVED_KEYWORDS))
