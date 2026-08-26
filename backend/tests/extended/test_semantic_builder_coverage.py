"""
Focused Unit Tests for Phase 1 — Specification Semantic Builder.
Tests all edge cases, empty sections, invalid entries, port formats, metadata title, and source file resolution.
"""

import pytest
from app.domain.specification_ast.document_node import DocumentNode
from app.domain.specification_ast.section_node import SectionNode
from app.domain.specification_ast.keyvalue_node import KeyValueNode
from app.domain.specification_ast.listitem_node import ListItemNode
from app.domain.specification_ast.text_node import TextNode
from app.parsers.specification.semantic_builder import SpecificationSemanticBuilder
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


def test_semantic_builder_document_title_and_source_file():
    doc = DocumentNode(title="  My Specification Project  ", source_file="")
    # Child with source_file
    sec = SectionNode(name="Inputs", source_file="")
    entry = TextNode(value="clk: 1 bit", source_file="spec.md")
    sec.entries.append(entry)
    doc.children.append(sec)

    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()

    assert res.specification.metadata.project_name == "My Specification Project"
    assert res.specification.metadata.source_file == "spec.md"


def test_semantic_builder_empty_sections():
    doc = DocumentNode(title="Test")
    sec_meta = SectionNode(name="Description")
    sec_ports = SectionNode(name="Inputs")
    sec_reqs = SectionNode(name="Functional Requirements")

    doc.children.extend([sec_meta, sec_ports, sec_reqs])

    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()

    warn_codes = [d.code for d in res.diagnostics if d.severity == DiagnosticSeverity.WARNING]
    assert len(warn_codes) >= 3


def test_semantic_builder_invalid_metadata_section_entries():
    class DummyNode:
        line = 1
        column = 1
        source_file = "test.txt"

    doc = DocumentNode(title="Test")
    sec = SectionNode(name="Description")
    sec.entries.append(DummyNode())  # invalid entry node type

    doc.children.append(sec)
    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()

    # invalid section entry warning emitted
    assert any("unsupported AST node type" in d.message for d in res.diagnostics)


def test_semantic_builder_port_declaration_formats():
    doc = DocumentNode(title="Test")
    sec_in = SectionNode(name="Inputs")

    # ListItemNode with colon
    sec_in.entries.append(ListItemNode(value="- clk: clock input 1 bit"))
    # ListItemNode without colon
    sec_in.entries.append(ListItemNode(value="- rst_n"))
    # KeyValueNode
    sec_in.entries.append(KeyValueNode(key="data_in", value="8 bit data input"))
    # Empty name port (e.g., just bullet or whitespace)
    sec_in.entries.append(TextNode(value="- : empty name"))

    doc.children.append(sec_in)
    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()

    ports = {p.name: p for p in res.specification.ports}
    assert "clk" in ports
    assert ports["clk"].width == 1
    assert "rst_n" in ports
    assert ports["rst_n"].width == 1
    assert "data_in" in ports
    assert ports["data_in"].width == 8


def test_semantic_builder_requirement_and_collection_node_types():
    doc = DocumentNode(title="Test")

    # Functional Requirements section
    sec_req = SectionNode(name="Functional Requirements")
    sec_req.entries.append(TextNode(value="REQ-1: Shall reset synchronously"))
    sec_req.entries.append(ListItemNode(value="- REQ-2: Shall process data"))
    sec_req.entries.append(KeyValueNode(key="REQ-3", value="Shall assert ready"))

    class InvalidReqNode:
        line = 1
        column = 1
        source_file = ""

    sec_req.entries.append(InvalidReqNode())

    # Parameters section (collection value test)
    sec_param = SectionNode(name="Parameters")
    sec_param.entries.append(ListItemNode(value="DATA_WIDTH"))
    sec_param.entries.append(KeyValueNode(key="DEPTH", value="16"))
    sec_param.entries.append(KeyValueNode(key="ONLY_KEY", value=""))
    sec_param.entries.append(InvalidReqNode())

    doc.children.extend([sec_req, sec_param])
    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()

    assert len(res.specification.requirements) == 3
    assert "DATA_WIDTH" in res.specification.parameters
    assert "DEPTH: 16" in res.specification.parameters
    assert "ONLY_KEY" in res.specification.parameters


def test_semantic_builder_source_file_fallback_sections():
    doc = DocumentNode(title="Test")
    child_sec = SectionNode(name="Notes", source_file="sec.txt")
    doc.children.append(child_sec)

    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()
    assert res.specification.metadata.source_file == "sec.txt"


def test_semantic_builder_metadata_keyvalue_entries():
    doc = DocumentNode(title="Test")
    sec_desc = SectionNode(name="Description")
    sec_desc.entries.append(KeyValueNode(key="Summary", value="This is a test description."))

    doc.children.append(sec_desc)
    builder = SpecificationSemanticBuilder(doc)
    res = builder.build()

    assert res.specification.metadata.description == "This is a test description."
