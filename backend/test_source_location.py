"""
Focused regression tests for the shared SourceLocation contract.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import FrozenInstanceError
from io import StringIO
from typing import Callable

from app.shared.source_location import SourceLocation


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


def test_default_location_is_unknown_memory_location() -> None:
    location = SourceLocation()

    assert location.source_file == ""
    assert location.line == 0
    assert location.column == 0
    assert location.is_known is False
    assert str(location) == "<memory>"


def test_complete_source_location_is_preserved() -> None:
    location = SourceLocation(
        source_file="specification.txt",
        line=17,
        column=5,
    )

    assert location.source_file == "specification.txt"
    assert location.line == 17
    assert location.column == 5
    assert location.is_known is True
    assert str(location) == "specification.txt:17:5"


def test_partial_locations_have_stable_formatting() -> None:
    source_only = SourceLocation(source_file="specification.txt")
    line_only = SourceLocation(line=9)
    source_and_line = SourceLocation(
        source_file="specification.txt",
        line=9,
    )

    assert str(source_only) == "specification.txt"
    assert str(line_only) == "<memory>:9"
    assert str(source_and_line) == "specification.txt:9"


def test_locations_are_value_comparable_and_hashable() -> None:
    first = SourceLocation(
        source_file="specification.txt",
        line=3,
        column=2,
    )
    second = SourceLocation(
        source_file="specification.txt",
        line=3,
        column=2,
    )
    different = SourceLocation(
        source_file="specification.txt",
        line=4,
        column=2,
    )

    assert first == second
    assert hash(first) == hash(second)
    assert first != different
    assert len({first, second, different}) == 2


def test_locations_are_immutable() -> None:
    location = SourceLocation(
        source_file="specification.txt",
        line=1,
        column=1,
    )

    expect_exception(
        FrozenInstanceError,
        "cannot assign to field 'line'",
        lambda: setattr(location, "line", 2),
    )


def test_invalid_source_file_is_rejected() -> None:
    expect_exception(
        TypeError,
        "source_file must be a string.",
        lambda: SourceLocation(source_file=123),  # type: ignore[arg-type]
    )


def test_invalid_line_values_are_rejected() -> None:
    for invalid_line in (-1, True, 1.5, "1"):
        expect_exception(
            ValueError,
            "line must be an integer greater than or equal to 0.",
            lambda value=invalid_line: SourceLocation(
                line=value  # type: ignore[arg-type]
            ),
        )


def test_invalid_column_values_are_rejected() -> None:
    for invalid_column in (-1, True, 1.5, "1"):
        expect_exception(
            ValueError,
            "column must be an integer greater than or equal to 0.",
            lambda value=invalid_column: SourceLocation(
                column=value  # type: ignore[arg-type]
            ),
        )


def test_construction_has_no_debug_output() -> None:
    output = StringIO()

    with redirect_stdout(output):
        SourceLocation(
            source_file="specification.txt",
            line=1,
            column=1,
        )

    assert output.getvalue() == ""


def main() -> None:
    tests = (
        test_default_location_is_unknown_memory_location,
        test_complete_source_location_is_preserved,
        test_partial_locations_have_stable_formatting,
        test_locations_are_value_comparable_and_hashable,
        test_locations_are_immutable,
        test_invalid_source_file_is_rejected,
        test_invalid_line_values_are_rejected,
        test_invalid_column_values_are_rejected,
        test_construction_has_no_debug_output,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSourceLocation tests passed.")


if __name__ == "__main__":
    main()
