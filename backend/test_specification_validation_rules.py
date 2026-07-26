"""
Focused regression tests for production SpecificationIR validation rules.
"""

from app.domain.metadata import Metadata
from app.domain.port import Port
from app.domain.requirement import Requirement
from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.specification_validation_rules import (
    DuplicatePortNameRule,
    DuplicateRequirementIdRule,
    EmptyRequirementDescriptionRule,
    InvalidPortDirectionRule,
    InvalidPortWidthRule,
    MissingModuleNameRule,
    MissingPortsRule,
    MissingProjectNameRule,
    MissingRequirementsRule,
    default_specification_validation_rules,
)
from app.engines.rule_engine.validation_engine import ValidationEngine
from app.shared.source_location import SourceLocation


def _valid_specification() -> SpecificationIR:
    return SpecificationIR(
        metadata=Metadata(
            project_name="Multiplexer",
            module_name="mux2to1",
            source_file="specification.txt",
        ),
        ports=[
            Port(
                name="a",
                direction="input",
                width=1,
                source_location=SourceLocation(
                    source_file="specification.txt",
                    line=10,
                    column=1,
                ),
            ),
            Port(
                name="y",
                direction="output",
                width=1,
                source_location=SourceLocation(
                    source_file="specification.txt",
                    line=11,
                    column=1,
                ),
            ),
        ],
        requirements=[
            Requirement(
                requirement_id="REQ_001",
                category="Functional",
                description="Output y shall follow input a.",
                source_location=SourceLocation(
                    source_file="specification.txt",
                    line=15,
                    column=1,
                ),
            )
        ],
    )


def test_rule_metadata_and_default_order_are_stable() -> None:
    rules = default_specification_validation_rules()

    assert [type(rule) for rule in rules] == [
        MissingProjectNameRule,
        MissingModuleNameRule,
        MissingPortsRule,
        MissingRequirementsRule,
        InvalidPortDirectionRule,
        InvalidPortWidthRule,
        DuplicatePortNameRule,
        DuplicateRequirementIdRule,
        EmptyRequirementDescriptionRule,
    ]
    assert [rule.rule_id for rule in rules] == [
        "SPEC-RULE-001",
        "SPEC-RULE-002",
        "SPEC-RULE-003",
        "SPEC-RULE-004",
        "SPEC-RULE-005",
        "SPEC-RULE-006",
        "SPEC-RULE-007",
        "SPEC-RULE-008",
        "SPEC-RULE-009",
    ]
    assert all(rule.stage == "specification-validation" for rule in rules)


def test_valid_specification_produces_no_diagnostics() -> None:
    result = ValidationEngine(
        default_specification_validation_rules()
    ).run(_valid_specification())

    assert result.is_successful
    assert result.executed_rule_count == 9
    assert result.diagnostic_count == 0
    assert result.diagnostics == ()


def test_missing_top_level_information_is_reported_in_rule_order() -> None:
    specification = SpecificationIR(
        metadata=Metadata(source_file="empty_spec.txt")
    )

    result = ValidationEngine(
        default_specification_validation_rules()
    ).run(specification)

    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "SPEC-VAL-001",
        "SPEC-VAL-002",
        "SPEC-VAL-003",
        "SPEC-VAL-004",
    ]
    assert [
        diagnostic.severity for diagnostic in result.diagnostics
    ] == [
        DiagnosticSeverity.WARNING,
        DiagnosticSeverity.ERROR,
        DiagnosticSeverity.ERROR,
        DiagnosticSeverity.WARNING,
    ]
    assert all(
        diagnostic.source_file == "empty_spec.txt"
        for diagnostic in result.diagnostics
    )
    assert all(diagnostic.line == 0 for diagnostic in result.diagnostics)
    assert all(diagnostic.column == 0 for diagnostic in result.diagnostics)


def test_port_rule_diagnostics_preserve_source_order_and_location() -> None:
    specification = _valid_specification()
    specification.ports = [
        Port(
            name="data",
            direction="source",
            width=0,
            source_location=SourceLocation(
                source_file="ports.txt",
                line=20,
                column=3,
            ),
        ),
        Port(
            name="data",
            direction="output",
            width=True,
            source_location=SourceLocation(
                source_file="ports.txt",
                line=21,
                column=5,
            ),
        ),
    ]

    result = ValidationEngine(
        (
            InvalidPortDirectionRule(),
            InvalidPortWidthRule(),
            DuplicatePortNameRule(),
        )
    ).run(specification)

    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "SPEC-VAL-005",
        "SPEC-VAL-006",
        "SPEC-VAL-006",
        "SPEC-VAL-007",
    ]
    assert [
        (diagnostic.line, diagnostic.column)
        for diagnostic in result.diagnostics
    ] == [
        (20, 3),
        (20, 3),
        (21, 5),
        (21, 5),
    ]
    assert all(
        diagnostic.source_file == "ports.txt"
        for diagnostic in result.diagnostics
    )


def test_requirement_rule_diagnostics_preserve_source_order_and_location() -> None:
    specification = _valid_specification()
    specification.requirements = [
        Requirement(
            requirement_id="REQ_001",
            category="Functional",
            description="Valid requirement.",
            source_location=SourceLocation(
                source_file="requirements.txt",
                line=30,
                column=1,
            ),
        ),
        Requirement(
            requirement_id="REQ_001",
            category="Functional",
            description="   ",
            source_location=SourceLocation(
                source_file="requirements.txt",
                line=31,
                column=2,
            ),
        ),
    ]

    result = ValidationEngine(
        (
            DuplicateRequirementIdRule(),
            EmptyRequirementDescriptionRule(),
        )
    ).run(specification)

    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "SPEC-VAL-008",
        "SPEC-VAL-009",
    ]
    assert [
        (diagnostic.line, diagnostic.column)
        for diagnostic in result.diagnostics
    ] == [
        (31, 2),
        (31, 2),
    ]


def test_default_rule_factory_and_runs_are_independent() -> None:
    first_rules = default_specification_validation_rules()
    second_rules = default_specification_validation_rules()

    assert first_rules is not second_rules
    assert all(
        first is not second
        for first, second in zip(first_rules, second_rules, strict=True)
    )

    engine = ValidationEngine(first_rules)
    specification = SpecificationIR()

    first_result = engine.run(specification)
    second_result = engine.run(specification)

    assert first_result is not second_result
    assert first_result.rule_results is not second_result.rule_results
    assert first_result.diagnostics == second_result.diagnostics


def main() -> None:
    tests = (
        test_rule_metadata_and_default_order_are_stable,
        test_valid_specification_produces_no_diagnostics,
        test_missing_top_level_information_is_reported_in_rule_order,
        test_port_rule_diagnostics_preserve_source_order_and_location,
        test_requirement_rule_diagnostics_preserve_source_order_and_location,
        test_default_rule_factory_and_runs_are_independent,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecification validation-rule tests passed.")


if __name__ == "__main__":
    main()
