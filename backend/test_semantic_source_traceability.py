"""
Focused regression tests for semantic-domain source traceability.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from typing import Callable

from app.domain.port import Port
from app.domain.requirement import Requirement
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


def test_legacy_port_construction_remains_compatible() -> None:
    port = Port(
        name="clk",
        direction="input",
        datatype="logic",
        width=1,
    )

    assert port.name == "clk"
    assert port.direction == "input"
    assert port.datatype == "logic"
    assert port.width == 1
    assert port.source_location == SourceLocation()
    assert port.source_location.is_known is False


def test_port_preserves_explicit_source_location() -> None:
    location = SourceLocation(
        source_file="specification.txt",
        line=10,
        column=1,
    )

    port = Port(
        name="data",
        direction="input",
        width=32,
        description="32-bit input",
        source_location=location,
    )

    assert port.source_location is location
    assert str(port.source_location) == "specification.txt:10:1"


def test_legacy_requirement_construction_remains_compatible() -> None:
    requirement = Requirement(
        requirement_id="REQ_001",
        category="Functional",
        description="Output shall follow the selected input.",
    )

    assert requirement.requirement_id == "REQ_001"
    assert requirement.category == "Functional"
    assert requirement.priority == "MEDIUM"
    assert requirement.verification_status == "NOT_VERIFIED"
    assert requirement.source_location == SourceLocation()
    assert requirement.source_location.is_known is False


def test_requirement_preserves_explicit_source_location() -> None:
    location = SourceLocation(
        source_file="specification.txt",
        line=18,
        column=1,
    )

    requirement = Requirement(
        requirement_id="REQ_001",
        category="Functional",
        description="Output shall equal input a when sel is zero.",
        source_section="Functional Requirements",
        source_location=location,
    )

    assert requirement.source_section == "Functional Requirements"
    assert requirement.source_location is location
    assert str(requirement.source_location) == "specification.txt:18:1"


def test_default_source_locations_are_independent() -> None:
    first_port = Port(name="a", direction="input")
    second_port = Port(name="b", direction="input")

    first_requirement = Requirement(
        requirement_id="REQ_001",
        category="Functional",
        description="First requirement.",
    )
    second_requirement = Requirement(
        requirement_id="REQ_002",
        category="Functional",
        description="Second requirement.",
    )

    assert first_port.source_location is not second_port.source_location
    assert (
        first_requirement.source_location
        is not second_requirement.source_location
    )


def test_invalid_port_source_location_is_rejected() -> None:
    expect_exception(
        TypeError,
        "source_location must be a SourceLocation.",
        lambda: Port(
            name="clk",
            direction="input",
            source_location="line 1",  # type: ignore[arg-type]
        ),
    )


def test_invalid_requirement_source_location_is_rejected() -> None:
    expect_exception(
        TypeError,
        "source_location must be a SourceLocation.",
        lambda: Requirement(
            requirement_id="REQ_001",
            category="Functional",
            description="Requirement.",
            source_location="line 1",  # type: ignore[arg-type]
        ),
    )


def test_construction_has_no_debug_output() -> None:
    output = StringIO()

    with redirect_stdout(output):
        Port(
            name="clk",
            direction="input",
            source_location=SourceLocation(line=1, column=1),
        )
        Requirement(
            requirement_id="REQ_001",
            category="Functional",
            description="Requirement.",
            source_location=SourceLocation(line=2, column=1),
        )

    assert output.getvalue() == ""


def main() -> None:
    tests = (
        test_legacy_port_construction_remains_compatible,
        test_port_preserves_explicit_source_location,
        test_legacy_requirement_construction_remains_compatible,
        test_requirement_preserves_explicit_source_location,
        test_default_source_locations_are_independent,
        test_invalid_port_source_location_is_rejected,
        test_invalid_requirement_source_location_is_rejected,
        test_construction_has_no_debug_output,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSemantic source-traceability tests passed.")


if __name__ == "__main__":
    main()
