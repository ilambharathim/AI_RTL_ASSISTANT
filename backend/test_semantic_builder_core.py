"""
Core regression tests for the specification semantic builder.
"""

from __future__ import annotations

from typing import Callable

from app.domain.ast.document_node import DocumentNode
from app.domain.ast.keyvalue_node import KeyValueNode
from app.domain.ast.listitem_node import ListItemNode
from app.domain.ast.section_node import SectionNode
from app.domain.ast.text_node import TextNode
from app.parsers.specification.semantic_builder import (
    SpecificationSemanticBuilder,
)


SOURCE_FILE = "uploads/specifications/specification.txt"


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


def make_sample_document() -> DocumentNode:
    document = DocumentNode(source_file=SOURCE_FILE)

    document.add_entry(
        KeyValueNode(
            key="Project Title",
            value="2-to-1 Multiplexer",
            line=1,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    module_section = SectionNode(
        name="Module Name",
        line=3,
        column=1,
        source_file=SOURCE_FILE,
    )
    module_section.add_entry(
        ListItemNode(
            value="mux2to1",
            line=4,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(module_section)

    description_section = SectionNode(
        name="Description",
        line=6,
        column=1,
        source_file=SOURCE_FILE,
    )
    description_section.add_entry(
        TextNode(
            value="Design a combinational 2-to-1 multiplexer.",
            line=7,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(description_section)

    inputs_section = SectionNode(
        name="Inputs",
        line=9,
        column=1,
        source_file=SOURCE_FILE,
    )
    inputs_section.add_entry(
        KeyValueNode(
            key="- a",
            value="1-bit input",
            line=10,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    inputs_section.add_entry(
        KeyValueNode(
            key="- b",
            value="1-bit input",
            line=11,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    inputs_section.add_entry(
        KeyValueNode(
            key="- sel",
            value="1-bit select signal",
            line=12,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(inputs_section)

    output_section = SectionNode(
        name="Output",
        line=14,
        column=1,
        source_file=SOURCE_FILE,
    )
    output_section.add_entry(
        KeyValueNode(
            key="- y",
            value="1-bit output",
            line=15,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(output_section)

    requirements_section = SectionNode(
        name="Functional Requirements",
        line=17,
        column=1,
        source_file=SOURCE_FILE,
    )
    requirements_section.add_entry(
        TextNode(
            value=(
                "1. If sel = 0, output y shall be equal to input a."
            ),
            line=18,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    requirements_section.add_entry(
        TextNode(
            value=(
                "2. If sel = 1, output y shall be equal to input b."
            ),
            line=19,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(requirements_section)

    timing_section = SectionNode(
        name="Timing",
        line=21,
        column=1,
        source_file=SOURCE_FILE,
    )
    timing_section.add_entry(
        TextNode(
            value="Pure combinational logic.",
            line=22,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(timing_section)

    language_section = SectionNode(
        name="Language",
        line=24,
        column=1,
        source_file=SOURCE_FILE,
    )
    language_section.add_entry(
        ListItemNode(
            value="SystemVerilog",
            line=25,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(language_section)

    return document


def test_builder_requires_document_node() -> None:
    expect_exception(
        TypeError,
        "document must be a DocumentNode.",
        lambda: SpecificationSemanticBuilder(
            "invalid"  # type: ignore[arg-type]
        ),
    )


def test_sample_document_maps_to_specification_ir() -> None:
    result = SpecificationSemanticBuilder(
        make_sample_document()
    ).build()

    specification = result.specification

    assert result.diagnostics == ()
    assert result.is_successful is True

    assert specification.metadata.project_name == "2-to-1 Multiplexer"
    assert specification.metadata.module_name == "mux2to1"
    assert (
        specification.metadata.description
        == "Design a combinational 2-to-1 multiplexer."
    )
    assert specification.metadata.language == "SystemVerilog"
    assert specification.metadata.source_file == SOURCE_FILE
    assert specification.metadata.created_at is None

    assert [port.name for port in specification.ports] == [
        "a",
        "b",
        "sel",
        "y",
    ]
    assert [port.direction for port in specification.ports] == [
        "input",
        "input",
        "input",
        "output",
    ]
    assert [port.width for port in specification.ports] == [
        1,
        1,
        1,
        1,
    ]
    assert specification.ports[0].description == "1-bit input"
    assert specification.ports[0].source_location.line == 10
    assert specification.ports[3].source_location.line == 15

    assert [
        requirement.requirement_id
        for requirement in specification.requirements
    ] == ["REQ_001", "REQ_002"]
    assert [
        requirement.description
        for requirement in specification.requirements
    ] == [
        "If sel = 0, output y shall be equal to input a.",
        "If sel = 1, output y shall be equal to input b.",
    ]
    assert all(
        requirement.category == "Functional"
        for requirement in specification.requirements
    )
    assert specification.requirements[0].source_location.line == 18
    assert specification.requirements[1].source_location.line == 19

    assert specification.timing_requirements == [
        "Pure combinational logic."
    ]


def test_repeated_builds_are_equal_and_independent() -> None:
    builder = SpecificationSemanticBuilder(make_sample_document())

    first = builder.build()
    second = builder.build()

    assert first == second
    assert first is not second
    assert first.specification is not second.specification
    assert (
        first.specification.metadata
        is not second.specification.metadata
    )
    assert first.specification.ports is not second.specification.ports
    assert (
        first.specification.requirements
        is not second.specification.requirements
    )

    first.specification.ports.clear()

    assert len(first.specification.ports) == 0
    assert len(second.specification.ports) == 4


def test_missing_module_name_is_reported() -> None:
    document = DocumentNode(source_file=SOURCE_FILE)
    document.add_entry(
        KeyValueNode(
            key="Project Title",
            value="Incomplete Specification",
            line=1,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    result = SpecificationSemanticBuilder(document).build()

    assert result.error_count == 1
    assert result.has_errors is True
    assert result.diagnostics[0].code == "SPEC-SEM-012"
    assert (
        result.diagnostics[0].stage
        == "specification-semantic-builder"
    )
    assert result.diagnostics[0].source_file == SOURCE_FILE


def main() -> None:
    tests = (
        test_builder_requires_document_node,
        test_sample_document_maps_to_specification_ir,
        test_repeated_builds_are_equal_and_independent,
        test_missing_module_name_is_reported,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSemantic builder core tests passed.")


if __name__ == "__main__":
    main()
