"""
Focused Unit Tests for Phase 5 — RTL Graph Builder.
Tests StatementBlock, IfStatement, UnaryExpression, None nodes, and graph structure.
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    StatementBlock,
    IfStatement,
    AlwaysBlock,
    ProceduralAssignment,
    ContinuousAssign,
)
from app.ast.expression import (
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
    LiteralExpression,
)
from app.elaboration.rtl_graph.rtl_graph_builder import RTLGraphBuilder
from app.semantics.semantic_model import SemanticModel


def test_rtl_graph_builder_statement_block_and_if_statement():
    # assign a = !b; inside if (c) inside StatementBlock inside AlwaysBlock
    assign_a = ProceduralAssignment(
        target="a",
        operator="=",
        expression=UnaryExpression(operator="!", operand=IdentifierExpression("b")),
    )
    assign_d = ProceduralAssignment(
        target="d",
        operator="=",
        expression=BinaryExpression(
            left=IdentifierExpression("e"),
            operator="+",
            right=IdentifierExpression("f"),
        ),
    )

    if_stmt = IfStatement(
        condition=IdentifierExpression("c"),
        then_branch=assign_a,
        else_branch=assign_d,
    )

    sb = StatementBlock(statements=(if_stmt,))
    always = AlwaysBlock(block_type="always_comb", sensitivity=[], statements=[sb])

    mod_decl = ModuleDeclaration(name="top", ports=[], members=[always])

    class DummyResolvedModule:
        name = "top"
        declaration = mod_decl
        rtl_graph = None

    class DummyBoundHierarchy:
        modules = {}

    model = SemanticModel()
    model.elaboration.elaborated_modules = {"top": DummyResolvedModule()}
    model.elaboration.port_bindings = DummyBoundHierarchy()

    builder = RTLGraphBuilder()
    builder.build(model)

    graph = model.elaboration.rtl_graph["top"]
    assert "a" in graph["adjacency"]
    assert "b" in graph["adjacency"]["a"]
    assert "d" in graph["adjacency"]
    assert "e" in graph["adjacency"]["d"]
    assert "f" in graph["adjacency"]["d"]


def test_rtl_graph_builder_null_handling():
    builder = RTLGraphBuilder()
    graph = {"adjacency": {}}

    # _visit None
    builder._visit(None, graph)

    # _collect_sources None
    sources = []
    builder._collect_sources(None, sources)
    assert sources == []
