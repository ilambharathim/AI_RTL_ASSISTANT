"""
Deterministic semantic transformation from generic specification AST to IR.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.domain.ast.ast_node import ASTNode
from app.domain.ast.document_node import DocumentNode
from app.domain.ast.keyvalue_node import KeyValueNode
from app.domain.ast.listitem_node import ListItemNode
from app.domain.ast.section_node import SectionNode
from app.domain.ast.text_node import TextNode
from app.domain.metadata import Metadata
from app.domain.port import Port
from app.domain.requirement import Requirement
from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.parsers.specification.semantic_diagnostic_code import (
    SpecificationSemanticDiagnosticCode,
)
from app.parsers.specification.semantic_result import (
    SpecificationSemanticResult,
)
from app.shared.source_location import SourceLocation


@dataclass(slots=True)
class _SemanticBuildState:
    """
    Isolated mutable state for one semantic build operation.
    """

    specification: SpecificationIR = field(default_factory=SpecificationIR)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    metadata_sources: dict[str, ASTNode] = field(default_factory=dict)
    port_names: set[str] = field(default_factory=set)
    next_requirement_index: int = 1


class SpecificationSemanticBuilder:
    """
    Converts a generic specification AST into a SpecificationIR.

    The builder recognizes a deliberately limited hardware-specification
    vocabulary. Unknown content is reported rather than silently interpreted.
    Repeated calls create independent deterministic results.
    """

    DIAGNOSTIC_STAGE = "specification-semantic-builder"

    _METADATA_LABELS = {
        "project title": "project_name",
        "project name": "project_name",
        "module name": "module_name",
        "description": "description",
        "language": "language",
        "version": "version",
        "author": "author",
        "organization": "organization",
    }

    _PORT_SECTIONS = {
        "input": "input",
        "inputs": "input",
        "output": "output",
        "outputs": "output",
        "inout": "inout",
        "inouts": "inout",
    }

    _REQUIREMENT_SECTIONS = {
        "functional requirement": "Functional",
        "functional requirements": "Functional",
        "requirement": "General",
        "requirements": "General",
    }

    _COLLECTION_SECTIONS = {
        "parameter": "parameters",
        "parameters": "parameters",
        "timing": "timing_requirements",
        "timing requirement": "timing_requirements",
        "timing requirements": "timing_requirements",
        "constraint": "constraints",
        "constraints": "constraints",
        "assertion": "assertions",
        "assertions": "assertions",
        "protocol": "protocols",
        "protocols": "protocols",
    }

    _SIMPLE_IDENTIFIER_PATTERN = re.compile(
        r"^[A-Za-z_][A-Za-z0-9_$]*$"
    )
    _BIT_WIDTH_PATTERN = re.compile(
        r"\b([0-9]+)\s*(?:-\s*)?bit\b",
        re.IGNORECASE,
    )
    _BULLET_PREFIX_PATTERN = re.compile(
        r"^\s*[-*•]\s*"
    )
    _ORDINAL_PREFIX_PATTERN = re.compile(
        r"^\s*[0-9]+[.)]\s*"
    )

    def __init__(self, document: DocumentNode) -> None:
        if not isinstance(document, DocumentNode):
            raise TypeError("document must be a DocumentNode.")

        self._document = document

    def build(self) -> SpecificationSemanticResult:
        """
        Build a fresh SpecificationIR and ordered semantic diagnostics.
        """

        state = _SemanticBuildState()
        state.specification.metadata.source_file = (
            self._find_source_file()
        )

        if self._document.title.strip():
            self._assign_metadata(
                field_name="project_name",
                value=self._document.title,
                node=self._document,
                state=state,
            )

        for child in self._document.children:
            if isinstance(child, SectionNode):
                self._process_section(child, state)
            else:
                self._process_document_entry(child, state)

        if not state.specification.metadata.module_name.strip():
            state.diagnostics.append(
                self._make_diagnostic(
                    code=(
                        SpecificationSemanticDiagnosticCode
                        .MISSING_MODULE_NAME
                    ),
                    message=(
                        "The specification does not define a module name."
                    ),
                    severity=DiagnosticSeverity.ERROR,
                    node=self._document,
                )
            )

        return SpecificationSemanticResult(
            specification=state.specification,
            diagnostics=tuple(state.diagnostics),
        )

    def _process_document_entry(
        self,
        entry: ASTNode,
        state: _SemanticBuildState,
    ) -> None:
        if isinstance(entry, KeyValueNode):
            normalized_key = self._normalize_label(entry.key)
            field_name = self._METADATA_LABELS.get(normalized_key)

            if field_name is not None:
                self._assign_metadata(
                    field_name=field_name,
                    value=entry.value,
                    node=entry,
                    state=state,
                )
                return

        state.diagnostics.append(
            self._make_diagnostic(
                code=(
                    SpecificationSemanticDiagnosticCode
                    .UNKNOWN_DOCUMENT_ENTRY
                ),
                message=(
                    "Document-level entry is not part of the recognized "
                    "semantic vocabulary."
                ),
                severity=DiagnosticSeverity.INFO,
                node=entry,
            )
        )

    def _process_section(
        self,
        section: SectionNode,
        state: _SemanticBuildState,
    ) -> None:
        normalized_name = self._normalize_label(section.name)

        metadata_field = self._METADATA_LABELS.get(normalized_name)
        if metadata_field is not None:
            self._process_metadata_section(
                section=section,
                field_name=metadata_field,
                state=state,
            )
            return

        port_direction = self._PORT_SECTIONS.get(normalized_name)
        if port_direction is not None:
            self._process_port_section(
                section=section,
                direction=port_direction,
                state=state,
            )
            return

        requirement_category = self._REQUIREMENT_SECTIONS.get(
            normalized_name
        )
        if requirement_category is not None:
            self._process_requirement_section(
                section=section,
                category=requirement_category,
                state=state,
            )
            return

        collection_field = self._COLLECTION_SECTIONS.get(
            normalized_name
        )
        if collection_field is not None:
            self._process_collection_section(
                section=section,
                field_name=collection_field,
                state=state,
            )
            return

        state.diagnostics.append(
            self._make_diagnostic(
                code=SpecificationSemanticDiagnosticCode.UNKNOWN_SECTION,
                message=(
                    f"Section '{section.name}' is not part of the "
                    "recognized semantic vocabulary."
                ),
                severity=DiagnosticSeverity.WARNING,
                node=section,
            )
        )

    def _process_metadata_section(
        self,
        section: SectionNode,
        field_name: str,
        state: _SemanticBuildState,
    ) -> None:
        if not section.entries:
            self._report_empty_section(section, state)
            return

        values: list[tuple[str, ASTNode]] = []

        for entry in section.entries:
            value = self._extract_scalar_value(entry)

            if value is None:
                self._report_invalid_section_entry(
                    section=section,
                    entry=entry,
                    state=state,
                )
                continue

            values.append((value, entry))

        if not values:
            return

        if field_name == "description":
            combined_value = "\n".join(
                value.strip()
                for value, _ in values
                if value.strip()
            )
            self._assign_metadata(
                field_name=field_name,
                value=combined_value,
                node=values[0][1],
                state=state,
            )
            return

        for value, entry in values:
            self._assign_metadata(
                field_name=field_name,
                value=value,
                node=entry,
                state=state,
            )

    def _process_port_section(
        self,
        section: SectionNode,
        direction: str,
        state: _SemanticBuildState,
    ) -> None:
        if not section.entries:
            self._report_empty_section(section, state)
            return

        for entry in section.entries:
            declaration = self._extract_port_declaration(entry)

            if declaration is None:
                state.diagnostics.append(
                    self._make_diagnostic(
                        code=(
                            SpecificationSemanticDiagnosticCode
                            .INVALID_PORT_DECLARATION
                        ),
                        message=(
                            f"Entry in section '{section.name}' is not a "
                            "valid port declaration."
                        ),
                        severity=DiagnosticSeverity.ERROR,
                        node=entry,
                    )
                )
                continue

            name, description = declaration

            if not self._SIMPLE_IDENTIFIER_PATTERN.fullmatch(name):
                state.diagnostics.append(
                    self._make_diagnostic(
                        code=(
                            SpecificationSemanticDiagnosticCode
                            .INVALID_PORT_NAME
                        ),
                        message=f"Port name '{name}' is not valid.",
                        severity=DiagnosticSeverity.ERROR,
                        node=entry,
                    )
                )
                continue

            if name in state.port_names:
                state.diagnostics.append(
                    self._make_diagnostic(
                        code=(
                            SpecificationSemanticDiagnosticCode
                            .DUPLICATE_PORT
                        ),
                        message=(
                            f"Port '{name}' was already declared; the "
                            "first declaration is preserved."
                        ),
                        severity=DiagnosticSeverity.ERROR,
                        node=entry,
                    )
                )
                continue

            width = self._extract_port_width(
                description=description,
                node=entry,
                state=state,
            )

            state.specification.ports.append(
                Port(
                    name=name,
                    direction=direction,
                    width=width,
                    description=description,
                    source_location=self._source_location(entry),
                )
            )
            state.port_names.add(name)

    def _process_requirement_section(
        self,
        section: SectionNode,
        category: str,
        state: _SemanticBuildState,
    ) -> None:
        if not section.entries:
            self._report_empty_section(section, state)
            return

        for entry in section.entries:
            description = self._extract_requirement_text(entry)

            if description is None or not description.strip():
                state.diagnostics.append(
                    self._make_diagnostic(
                        code=(
                            SpecificationSemanticDiagnosticCode
                            .EMPTY_REQUIREMENT
                        ),
                        message=(
                            f"Section '{section.name}' contains an empty "
                            "requirement."
                        ),
                        severity=DiagnosticSeverity.WARNING,
                        node=entry,
                    )
                )
                continue

            requirement_id = (
                f"REQ_{state.next_requirement_index:03d}"
            )
            state.next_requirement_index += 1

            state.specification.requirements.append(
                Requirement(
                    requirement_id=requirement_id,
                    category=category,
                    description=description,
                    source_section=section.name,
                    source_location=self._source_location(entry),
                )
            )

    def _process_collection_section(
        self,
        section: SectionNode,
        field_name: str,
        state: _SemanticBuildState,
    ) -> None:
        if not section.entries:
            self._report_empty_section(section, state)
            return

        target = getattr(state.specification, field_name)

        for entry in section.entries:
            value = self._extract_collection_value(entry)

            if value is None:
                self._report_invalid_section_entry(
                    section=section,
                    entry=entry,
                    state=state,
                )
                continue

            target.append(value)

    def _assign_metadata(
        self,
        field_name: str,
        value: str,
        node: ASTNode,
        state: _SemanticBuildState,
    ) -> None:
        normalized_value = value.strip()

        if not normalized_value:
            state.diagnostics.append(
                self._make_diagnostic(
                    code=(
                        SpecificationSemanticDiagnosticCode
                        .EMPTY_METADATA_VALUE
                    ),
                    message=(
                        f"Metadata field '{field_name}' has an empty value."
                    ),
                    severity=DiagnosticSeverity.WARNING,
                    node=node,
                )
            )
            return

        if field_name in state.metadata_sources:
            state.diagnostics.append(
                self._make_diagnostic(
                    code=(
                        SpecificationSemanticDiagnosticCode
                        .DUPLICATE_METADATA_FIELD
                    ),
                    message=(
                        f"Metadata field '{field_name}' was already "
                        "assigned; the first value is preserved."
                    ),
                    severity=DiagnosticSeverity.WARNING,
                    node=node,
                )
            )
            return

        metadata: Metadata = state.specification.metadata
        setattr(metadata, field_name, normalized_value)
        state.metadata_sources[field_name] = node

    def _extract_port_declaration(
        self,
        entry: ASTNode,
    ) -> tuple[str, str] | None:
        if isinstance(entry, KeyValueNode):
            raw_name = entry.key
            description = entry.value.strip()
        elif isinstance(entry, (ListItemNode, TextNode)):
            raw_value = entry.value.strip()

            if ":" in raw_value:
                raw_name, description = raw_value.split(":", 1)
                description = description.strip()
            else:
                raw_name = raw_value
                description = ""
        else:
            return None

        name = self._strip_bullet_prefix(raw_name).strip()

        if not name:
            return None

        return name, description

    def _extract_port_width(
        self,
        description: str,
        node: ASTNode,
        state: _SemanticBuildState,
    ) -> int:
        matches = list(
            self._BIT_WIDTH_PATTERN.finditer(description)
        )

        if not matches:
            return 1

        if len(matches) > 1:
            state.diagnostics.append(
                self._make_diagnostic(
                    code=(
                        SpecificationSemanticDiagnosticCode
                        .INVALID_PORT_WIDTH
                    ),
                    message=(
                        "Port description contains multiple width "
                        "declarations; width defaults to 1."
                    ),
                    severity=DiagnosticSeverity.WARNING,
                    node=node,
                )
            )
            return 1

        width = int(matches[0].group(1))

        if width < 1:
            state.diagnostics.append(
                self._make_diagnostic(
                    code=(
                        SpecificationSemanticDiagnosticCode
                        .INVALID_PORT_WIDTH
                    ),
                    message=(
                        "Port width must be greater than zero; width "
                        "defaults to 1."
                    ),
                    severity=DiagnosticSeverity.WARNING,
                    node=node,
                )
            )
            return 1

        return width

    def _extract_requirement_text(
        self,
        entry: ASTNode,
    ) -> str | None:
        if isinstance(entry, (TextNode, ListItemNode)):
            value = entry.value
        elif isinstance(entry, KeyValueNode):
            value = entry.value or entry.key
        else:
            return None

        value = self._strip_bullet_prefix(value)
        value = self._ORDINAL_PREFIX_PATTERN.sub("", value)
        return value.strip()

    @staticmethod
    def _extract_scalar_value(entry: ASTNode) -> str | None:
        if isinstance(entry, (TextNode, ListItemNode)):
            return entry.value

        if isinstance(entry, KeyValueNode):
            return entry.value

        return None

    @staticmethod
    def _extract_collection_value(entry: ASTNode) -> str | None:
        if isinstance(entry, (TextNode, ListItemNode)):
            return entry.value.strip()

        if isinstance(entry, KeyValueNode):
            key = entry.key.strip()
            value = entry.value.strip()

            if value:
                return f"{key}: {value}"

            return key

        return None

    def _report_empty_section(
        self,
        section: SectionNode,
        state: _SemanticBuildState,
    ) -> None:
        state.diagnostics.append(
            self._make_diagnostic(
                code=SpecificationSemanticDiagnosticCode.EMPTY_SECTION,
                message=f"Section '{section.name}' is empty.",
                severity=DiagnosticSeverity.WARNING,
                node=section,
            )
        )

    def _report_invalid_section_entry(
        self,
        section: SectionNode,
        entry: ASTNode,
        state: _SemanticBuildState,
    ) -> None:
        state.diagnostics.append(
            self._make_diagnostic(
                code=(
                    SpecificationSemanticDiagnosticCode
                    .INVALID_SECTION_ENTRY
                ),
                message=(
                    f"Entry in section '{section.name}' has an "
                    "unsupported AST node type."
                ),
                severity=DiagnosticSeverity.WARNING,
                node=entry,
            )
        )

    def _make_diagnostic(
        self,
        code: SpecificationSemanticDiagnosticCode,
        message: str,
        severity: DiagnosticSeverity,
        node: ASTNode,
    ) -> Diagnostic:
        return Diagnostic(
            code=code.value,
            message=message,
            severity=severity,
            stage=self.DIAGNOSTIC_STAGE,
            line=node.line,
            column=node.column,
            source_file=node.source_file,
        )

    def _find_source_file(self) -> str | None:
        if self._document.source_file:
            return self._document.source_file

        for child in self._document.children:
            if child.source_file:
                return child.source_file

            if isinstance(child, SectionNode):
                for entry in child.entries:
                    if entry.source_file:
                        return entry.source_file

        return None

    @classmethod
    def _strip_bullet_prefix(cls, value: str) -> str:
        return cls._BULLET_PREFIX_PATTERN.sub("", value, count=1)

    @staticmethod
    def _normalize_label(value: str) -> str:
        return " ".join(value.strip().casefold().split())

    @staticmethod
    def _source_location(node: ASTNode) -> SourceLocation:
        return SourceLocation(
            source_file=node.source_file,
            line=node.line,
            column=node.column,
        )
