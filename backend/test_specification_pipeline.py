"""
End-to-end regression tests for the specification frontend pipeline.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from app.parsers.specification.lexer import SpecificationLexer
from app.parsers.specification.normalizer import DocumentNormalizer
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.reader import SpecificationReader
from app.parsers.specification.semantic_builder import (
    SpecificationSemanticBuilder,
)


SPECIFICATION_TEXT = """Project Title: 2-to-1 Multiplexer

Module Name:
mux2to1

Description:
Design a combinational 2-to-1 multiplexer.

Inputs:
- a : 1-bit input
- b : 1-bit input
- sel : 1-bit select signal

Output:
- y : 1-bit output

Functional Requirements:
1. If sel = 0, output y shall be equal to input a.
2. If sel = 1, output y shall be equal to input b.

Timing:
Pure combinational logic.

Language:
SystemVerilog
"""


def execute_pipeline(source_path: Path):
    """
    Execute the complete deterministic specification frontend.
    """

    source_file = source_path.as_posix()

    source_text = SpecificationReader.read(source_path)
    normalized_text = DocumentNormalizer.normalize(source_text)

    tokens = SpecificationLexer(
        normalized_text,
        source_file=source_file,
    ).tokenize()

    parse_result = SpecificationParser(
        tokens
    ).parse_with_diagnostics()

    semantic_result = SpecificationSemanticBuilder(
        parse_result.document
    ).build()

    return (
        normalized_text,
        tokens,
        parse_result,
        semantic_result,
    )


def create_specification_file(directory: str) -> Path:
    """
    Create an isolated UTF-8 specification fixture.
    """

    source_path = Path(directory) / "specification.txt"
    source_path.write_text(
        SPECIFICATION_TEXT,
        encoding="utf-8",
    )
    return source_path


def test_complete_pipeline_maps_realistic_specification() -> None:
    with TemporaryDirectory() as directory:
        source_path = create_specification_file(directory)

        (
            normalized_text,
            tokens,
            parse_result,
            semantic_result,
        ) = execute_pipeline(source_path)

        specification = semantic_result.specification

        assert normalized_text == SPECIFICATION_TEXT.strip()
        assert len(tokens) == 54

        assert parse_result.diagnostics == ()
        assert parse_result.is_successful is True

        assert semantic_result.diagnostics == ()
        assert semantic_result.is_successful is True

        metadata = specification.metadata

        assert metadata.project_name == "2-to-1 Multiplexer"
        assert metadata.module_name == "mux2to1"
        assert (
            metadata.description
            == "Design a combinational 2-to-1 multiplexer."
        )
        assert metadata.language == "SystemVerilog"
        assert metadata.source_file == source_path.as_posix()
        assert metadata.created_at is None

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
        assert [port.description for port in specification.ports] == [
            "1-bit input",
            "1-bit input",
            "1-bit select signal",
            "1-bit output",
        ]

        assert [
            requirement.requirement_id
            for requirement in specification.requirements
        ] == [
            "REQ_001",
            "REQ_002",
        ]
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

        assert specification.timing_requirements == [
            "Pure combinational logic."
        ]


def test_pipeline_preserves_source_traceability() -> None:
    with TemporaryDirectory() as directory:
        source_path = create_specification_file(directory)

        _, _, _, semantic_result = execute_pipeline(source_path)

        specification = semantic_result.specification
        expected_source_file = source_path.as_posix()

        assert specification.metadata.source_file == expected_source_file

        assert [
            port.source_location.source_file
            for port in specification.ports
        ] == [
            expected_source_file,
            expected_source_file,
            expected_source_file,
            expected_source_file,
        ]
        assert [
            port.source_location.line
            for port in specification.ports
        ] == [
            10,
            11,
            12,
            15,
        ]
        assert [
            port.source_location.column
            for port in specification.ports
        ] == [
            1,
            1,
            1,
            1,
        ]

        assert [
            requirement.source_location.source_file
            for requirement in specification.requirements
        ] == [
            expected_source_file,
            expected_source_file,
        ]
        assert [
            requirement.source_location.line
            for requirement in specification.requirements
        ] == [
            18,
            19,
        ]
        assert [
            requirement.source_location.column
            for requirement in specification.requirements
        ] == [
            1,
            1,
        ]


def test_pipeline_is_deterministic_and_independent() -> None:
    with TemporaryDirectory() as directory:
        source_path = create_specification_file(directory)

        first = execute_pipeline(source_path)
        second = execute_pipeline(source_path)

        first_tokens = first[1]
        second_tokens = second[1]
        first_parse_result = first[2]
        second_parse_result = second[2]
        first_semantic_result = first[3]
        second_semantic_result = second[3]

        assert first_tokens == second_tokens
        assert first_tokens is not second_tokens

        assert first_parse_result == second_parse_result
        assert first_parse_result is not second_parse_result
        assert (
            first_parse_result.document
            is not second_parse_result.document
        )

        assert first_semantic_result == second_semantic_result
        assert first_semantic_result is not second_semantic_result
        assert (
            first_semantic_result.specification
            is not second_semantic_result.specification
        )
        assert (
            first_semantic_result.specification.metadata
            is not second_semantic_result.specification.metadata
        )
        assert (
            first_semantic_result.specification.ports
            is not second_semantic_result.specification.ports
        )
        assert (
            first_semantic_result.specification.requirements
            is not second_semantic_result.specification.requirements
        )

        first_semantic_result.specification.ports.clear()

        assert first_semantic_result.specification.ports == []
        assert len(second_semantic_result.specification.ports) == 4


def main() -> None:
    tests = (
        test_complete_pipeline_maps_realistic_specification,
        test_pipeline_preserves_source_traceability,
        test_pipeline_is_deterministic_and_independent,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecification pipeline integration tests passed.")


if __name__ == "__main__":
    main()
