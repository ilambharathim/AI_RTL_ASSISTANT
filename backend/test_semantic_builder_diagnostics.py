"""
Diagnostic regression tests for the specification semantic builder.
"""

from __future__ import annotations

from app.domain.specification_ast.ast_node import ASTNode
from app.domain.specification_ast.document_node import DocumentNode
from app.domain.specification_ast.keyvalue_node import KeyValueNode
from app.domain.specification_ast.section_node import SectionNode
from app.domain.specification_ast.text_node import TextNode
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.parsers.specification.semantic_builder import (
    SpecificationSemanticBuilder,
)


SOURCE_FILE = "diagnostic_specification.txt"


def make_diagnostic_document() -> DocumentNode:
    document = DocumentNode(source_file=SOURCE_FILE)

    document.add_entry(
        KeyValueNode(
            key="Module Name",
            value="diagnostic_module",
            line=1,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    document.add_entry(
        TextNode(
            value="Unrecognized document-level prose.",
            line=2,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    document.add_entry(
        KeyValueNode(
            key="Project Name",
            value="First Project Name",
            line=3,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    document.add_entry(
        KeyValueNode(
            key="Project Title",
            value="Second Project Name",
            line=4,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    document.add_entry(
        KeyValueNode(
            key="Author",
            value="",
            line=5,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    unknown_section = SectionNode(
        name="Unsupported Section",
        line=6,
        column=1,
        source_file=SOURCE_FILE,
    )
    document.add_section(unknown_section)

    constraints_section = SectionNode(
        name="Constraints",
        line=7,
        column=1,
        source_file=SOURCE_FILE,
    )
    constraints_section.add_entry(
        ASTNode(
            node_type="CUSTOM",
            line=8,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(constraints_section)

    empty_protocols_section = SectionNode(
        name="Protocols",
        line=9,
        column=1,
        source_file=SOURCE_FILE,
    )
    document.add_section(empty_protocols_section)

    inputs_section = SectionNode(
        name="Inputs",
        line=10,
        column=1,
        source_file=SOURCE_FILE,
    )

    inputs_section.add_entry(
        ASTNode(
            node_type="CUSTOM",
            line=11,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    inputs_section.add_entry(
        KeyValueNode(
            key="- 9bad",
            value="1-bit input",
            line=12,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    inputs_section.add_entry(
        KeyValueNode(
            key="- a",
            value="8-bit input",
            line=13,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    inputs_section.add_entry(
        KeyValueNode(
            key="- a",
            value="8-bit duplicate input",
            line=14,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    inputs_section.add_entry(
        KeyValueNode(
            key="- zero_width",
            value="0-bit input",
            line=15,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    inputs_section.add_entry(
        KeyValueNode(
            key="- ambiguous",
            value="8-bit input connected to a 16-bit bus",
            line=16,
            column=1,
            source_file=SOURCE_FILE,
        )
    )

    document.add_section(inputs_section)

    requirements_section = SectionNode(
        name="Functional Requirements",
        line=17,
        column=1,
        source_file=SOURCE_FILE,
    )
    requirements_section.add_entry(
        KeyValueNode(
            key="-",
            value="",
            line=18,
            column=1,
            source_file=SOURCE_FILE,
        )
    )
    document.add_section(requirements_section)

    return document


def test_diagnostics_are_complete_and_source_ordered() -> None:
    result = SpecificationSemanticBuilder(
        make_diagnostic_document()
    ).build()

    expected_codes = (
        "SPEC-SEM-001",
        "SPEC-SEM-003",
        "SPEC-SEM-004",
        "SPEC-SEM-002",
        "SPEC-SEM-005",
        "SPEC-SEM-006",
        "SPEC-SEM-007",
        "SPEC-SEM-008",
        "SPEC-SEM-009",
        "SPEC-SEM-010",
        "SPEC-SEM-010",
        "SPEC-SEM-011",
    )
    expected_lines = (
        2,
        4,
        5,
        6,
        8,
        9,
        11,
        12,
        14,
        15,
        16,
        18,
    )
    expected_severities = (
        DiagnosticSeverity.INFO,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.ERROR,
        DiagnosticSeverity.ERROR,
        DiagnosticSeverity.ERROR,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.WARNING,
    )

    assert tuple(
        diagnostic.code
        for diagnostic in result.diagnostics
    ) == expected_codes

    assert tuple(
        diagnostic.line
        for diagnostic in result.diagnostics
    ) == expected_lines

    assert tuple(
        diagnostic.severity
        for diagnostic in result.diagnostics
    ) == expected_severities

    assert all(
        diagnostic.stage == "specification-semantic-builder"
        for diagnostic in result.diagnostics
    )
    assert all(
        diagnostic.source_file == SOURCE_FILE
        for diagnostic in result.diagnostics
    )

    assert result.diagnostic_count == 12
    assert result.error_count == 3
    assert result.warning_count == 8
    assert result.info_count == 1
    assert result.has_errors is True
    assert result.is_successful is False


def test_first_metadata_value_is_preserved() -> None:
    result = SpecificationSemanticBuilder(
        make_diagnostic_document()
    ).build()

    metadata = result.specification.metadata

    assert metadata.module_name == "diagnostic_module"
    assert metadata.project_name == "First Project Name"
    assert metadata.author is None
    assert metadata.source_file == SOURCE_FILE


def test_invalid_and_duplicate_ports_are_not_emitted() -> None:
    result = SpecificationSemanticBuilder(
        make_diagnostic_document()
    ).build()

    ports = result.specification.ports

    assert [port.name for port in ports] == [
        "a",
        "zero_width",
        "ambiguous",
    ]
    assert [port.direction for port in ports] == [
        "input",
        "input",
        "input",
    ]
    assert [port.width for port in ports] == [
        8,
        1,
        1,
    ]
    assert [port.source_location.line for port in ports] == [
        13,
        15,
        16,
    ]


def test_empty_requirement_is_not_emitted() -> None:
    result = SpecificationSemanticBuilder(
        make_diagnostic_document()
    ).build()

    assert result.specification.requirements == []


def test_repeated_diagnostic_builds_are_deterministic() -> None:
    builder = SpecificationSemanticBuilder(
        make_diagnostic_document()
    )

    first = builder.build()
    second = builder.build()

    assert first == second
    assert first is not second
    assert first.specification is not second.specification
    assert first.diagnostics is not second.diagnostics


def main() -> None:
    tests = (
        test_diagnostics_are_complete_and_source_ordered,
        test_first_metadata_value_is_preserved,
        test_invalid_and_duplicate_ports_are_not_emitted,
        test_empty_requirement_is_not_emitted,
        test_repeated_diagnostic_builds_are_deterministic,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSemantic builder diagnostic tests passed.")


if __name__ == "__main__":
    main()
