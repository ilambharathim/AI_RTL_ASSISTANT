"""
Focused regression tests for the deterministic Metadata contract.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from typing import Callable

from app.domain.metadata import Metadata


def expect_exception(
    exception_type: type[BaseException],
    message: str,
    operation: Callable[[], object],
) -> None:
    try:
        operation()
    except exception_type as error:
        assert str(error) == message
    else:
        raise AssertionError(
            f"Expected {exception_type.__name__}: {message}"
        )


def test_default_metadata_is_deterministic() -> None:
    first = Metadata()
    second = Metadata()

    assert first == second
    assert first.created_at is None
    assert second.created_at is None


def test_legacy_construction_remains_compatible() -> None:
    metadata = Metadata(
        project_name="RIVA",
        module_name="mux2to1",
        description="2-to-1 Multiplexer",
        language="SystemVerilog",
        author="Ilam Bharathi",
    )

    assert metadata.project_name == "RIVA"
    assert metadata.module_name == "mux2to1"
    assert metadata.description == "2-to-1 Multiplexer"
    assert metadata.language == "SystemVerilog"
    assert metadata.author == "Ilam Bharathi"
    assert metadata.version == "1.0"
    assert metadata.created_at is None


def test_explicit_timestamp_is_preserved() -> None:
    timestamp = datetime(
        2026,
        7,
        26,
        9,
        30,
        tzinfo=timezone.utc,
    )

    metadata = Metadata(created_at=timestamp)

    assert metadata.created_at is timestamp


def test_tags_have_independent_defaults() -> None:
    first = Metadata()
    second = Metadata()

    first.tags.append("specification")

    assert first.tags == ["specification"]
    assert second.tags == []
    assert first.tags is not second.tags


def test_invalid_timestamp_is_rejected() -> None:
    expect_exception(
        TypeError,
        "created_at must be a datetime or None.",
        lambda: Metadata(
            created_at="2026-07-26"  # type: ignore[arg-type]
        ),
    )


def test_construction_has_no_debug_output() -> None:
    output = StringIO()

    with redirect_stdout(output):
        Metadata(
            project_name="RIVA",
            module_name="mux2to1",
        )

    assert output.getvalue() == ""


def main() -> None:
    tests = (
        test_default_metadata_is_deterministic,
        test_legacy_construction_remains_compatible,
        test_explicit_timestamp_is_preserved,
        test_tags_have_independent_defaults,
        test_invalid_timestamp_is_rejected,
        test_construction_has_no_debug_output,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nMetadata contract tests passed.")


if __name__ == "__main__":
    main()
