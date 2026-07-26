"""
Production deterministic validation rules for SpecificationIR.

Each concrete rule owns one stable rule identifier and emits diagnostics with
one stable SpecificationValidationDiagnosticCode. Rule and diagnostic order is
deterministic and follows source collection order.
"""

from app.domain.port import Port
from app.domain.requirement import Requirement
from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.validation_diagnostic_code import (
    SpecificationValidationDiagnosticCode,
)
from app.engines.rule_engine.validation_rule import ValidationRule
from app.shared.source_location import SourceLocation


_VALID_PORT_DIRECTIONS = frozenset({"input", "output", "inout"})


def _metadata_location(specification: SpecificationIR) -> SourceLocation:
    source_file = specification.metadata.source_file

    return SourceLocation(
        source_file=source_file if source_file is not None else "",
    )


def _diagnostic(
    *,
    code: SpecificationValidationDiagnosticCode,
    message: str,
    severity: DiagnosticSeverity,
    stage: str,
    location: SourceLocation,
) -> Diagnostic:
    return Diagnostic(
        code=code.value,
        message=message,
        severity=severity,
        stage=stage,
        source_file=location.source_file,
        line=location.line,
        column=location.column,
    )


class MissingProjectNameRule(ValidationRule):
    """Require a non-blank project name."""

    rule_id = "SPEC-RULE-001"
    description = "Require a project name."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        if specification.metadata.project_name.strip():
            return ()

        return (
            _diagnostic(
                code=(
                    SpecificationValidationDiagnosticCode
                    .MISSING_PROJECT_NAME
                ),
                message="Specification project name is missing.",
                severity=DiagnosticSeverity.WARNING,
                stage=self.stage,
                location=_metadata_location(specification),
            ),
        )


class MissingModuleNameRule(ValidationRule):
    """Require a non-blank hardware module name."""

    rule_id = "SPEC-RULE-002"
    description = "Require a module name."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        if specification.metadata.module_name.strip():
            return ()

        return (
            _diagnostic(
                code=(
                    SpecificationValidationDiagnosticCode
                    .MISSING_MODULE_NAME
                ),
                message="Specification module name is missing.",
                severity=DiagnosticSeverity.ERROR,
                stage=self.stage,
                location=_metadata_location(specification),
            ),
        )


class MissingPortsRule(ValidationRule):
    """Require at least one declared port."""

    rule_id = "SPEC-RULE-003"
    description = "Require at least one port."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        if specification.ports:
            return ()

        return (
            _diagnostic(
                code=SpecificationValidationDiagnosticCode.MISSING_PORTS,
                message="Specification declares no ports.",
                severity=DiagnosticSeverity.ERROR,
                stage=self.stage,
                location=_metadata_location(specification),
            ),
        )


class MissingRequirementsRule(ValidationRule):
    """Require at least one verification requirement."""

    rule_id = "SPEC-RULE-004"
    description = "Require at least one requirement."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        if specification.requirements:
            return ()

        return (
            _diagnostic(
                code=(
                    SpecificationValidationDiagnosticCode
                    .MISSING_REQUIREMENTS
                ),
                message="Specification declares no requirements.",
                severity=DiagnosticSeverity.WARNING,
                stage=self.stage,
                location=_metadata_location(specification),
            ),
        )


class InvalidPortDirectionRule(ValidationRule):
    """Reject port directions outside input, output, and inout."""

    rule_id = "SPEC-RULE-005"
    description = "Validate port directions."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []

        for port in specification.ports:
            normalized_direction = port.direction.strip().lower()

            if normalized_direction in _VALID_PORT_DIRECTIONS:
                continue

            diagnostics.append(
                _diagnostic(
                    code=(
                        SpecificationValidationDiagnosticCode
                        .INVALID_PORT_DIRECTION
                    ),
                    message=(
                        f"Port '{port.name}' has invalid direction "
                        f"'{port.direction}'."
                    ),
                    severity=DiagnosticSeverity.ERROR,
                    stage=self.stage,
                    location=port.source_location,
                )
            )

        return tuple(diagnostics)


class InvalidPortWidthRule(ValidationRule):
    """Reject non-integer, boolean, zero, and negative port widths."""

    rule_id = "SPEC-RULE-006"
    description = "Validate port widths."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []

        for port in specification.ports:
            if type(port.width) is int and port.width > 0:
                continue

            diagnostics.append(
                _diagnostic(
                    code=(
                        SpecificationValidationDiagnosticCode
                        .INVALID_PORT_WIDTH
                    ),
                    message=(
                        f"Port '{port.name}' has invalid width "
                        f"'{port.width}'."
                    ),
                    severity=DiagnosticSeverity.ERROR,
                    stage=self.stage,
                    location=port.source_location,
                )
            )

        return tuple(diagnostics)


class DuplicatePortNameRule(ValidationRule):
    """Report each port name occurrence after its first declaration."""

    rule_id = "SPEC-RULE-007"
    description = "Reject duplicate port names."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []
        first_ports: dict[str, Port] = {}

        for port in specification.ports:
            normalized_name = port.name.strip()
            first_port = first_ports.get(normalized_name)

            if first_port is None:
                first_ports[normalized_name] = port
                continue

            diagnostics.append(
                _diagnostic(
                    code=(
                        SpecificationValidationDiagnosticCode
                        .DUPLICATE_PORT_NAME
                    ),
                    message=(
                        f"Port name '{normalized_name}' is duplicated; "
                        "the first declaration is preserved."
                    ),
                    severity=DiagnosticSeverity.ERROR,
                    stage=self.stage,
                    location=port.source_location,
                )
            )

        return tuple(diagnostics)


class DuplicateRequirementIdRule(ValidationRule):
    """Report each requirement identifier after its first occurrence."""

    rule_id = "SPEC-RULE-008"
    description = "Reject duplicate requirement identifiers."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []
        first_requirements: dict[str, Requirement] = {}

        for requirement in specification.requirements:
            normalized_id = requirement.requirement_id.strip()
            first_requirement = first_requirements.get(normalized_id)

            if first_requirement is None:
                first_requirements[normalized_id] = requirement
                continue

            diagnostics.append(
                _diagnostic(
                    code=(
                        SpecificationValidationDiagnosticCode
                        .DUPLICATE_REQUIREMENT_ID
                    ),
                    message=(
                        f"Requirement identifier '{normalized_id}' "
                        "is duplicated; the first occurrence is preserved."
                    ),
                    severity=DiagnosticSeverity.ERROR,
                    stage=self.stage,
                    location=requirement.source_location,
                )
            )

        return tuple(diagnostics)


class EmptyRequirementDescriptionRule(ValidationRule):
    """Reject requirements whose descriptions are empty or whitespace."""

    rule_id = "SPEC-RULE-009"
    description = "Require requirement descriptions."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []

        for requirement in specification.requirements:
            if requirement.description.strip():
                continue

            diagnostics.append(
                _diagnostic(
                    code=(
                        SpecificationValidationDiagnosticCode
                        .EMPTY_REQUIREMENT_DESCRIPTION
                    ),
                    message=(
                        f"Requirement '{requirement.requirement_id}' "
                        "has an empty description."
                    ),
                    severity=DiagnosticSeverity.ERROR,
                    stage=self.stage,
                    location=requirement.source_location,
                )
            )

        return tuple(diagnostics)


def default_specification_validation_rules() -> tuple[ValidationRule, ...]:
    """
    Return a fresh, deterministic production rule set.

    Rule order is a released diagnostic-order contract.
    """

    return (
        MissingProjectNameRule(),
        MissingModuleNameRule(),
        MissingPortsRule(),
        MissingRequirementsRule(),
        InvalidPortDirectionRule(),
        InvalidPortWidthRule(),
        DuplicatePortNameRule(),
        DuplicateRequirementIdRule(),
        EmptyRequirementDescriptionRule(),
    )
