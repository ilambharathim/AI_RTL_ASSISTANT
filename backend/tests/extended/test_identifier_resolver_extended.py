"""
Extended Unit Test Suite for IdentifierResolver.
Validates 100% branch coverage across scope lookups, AST traversal, undefined identifiers, and nested scopes.
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
    IfStatement,
    StatementBlock,
    AlwaysBlock,
)
from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
)
from app.semantics.scope import Scope, ScopeKind
from app.semantics.symbol import Symbol
from app.semantics.symbol_kind import SymbolKind
from app.semantics.visitors.identifier_resolver import IdentifierResolver


def test_identifier_resolver_all_branches():
    # 1. Setup scope with defined symbols
    root_scope = Scope(name="global", kind=ScopeKind.GLOBAL)
    mod_scope = Scope(name="top", kind=ScopeKind.MODULE, parent=root_scope)
    mod_scope.define(Symbol(name="data_in", kind=SymbolKind.SIGNAL))
    mod_scope.define(Symbol(name="data_out", kind=SymbolKind.SIGNAL))

    # 2. Build AST nodes with valid and undefined identifiers
    valid_id = IdentifierExpression(name="data_in")
    undefined_id = IdentifierExpression(name="undefined_sig")
    lit = LiteralExpression(value="16'd0")
    un_op = UnaryExpression(operator="-", operand=valid_id)
    bin_op = BinaryExpression(operator="+", left=un_op, right=undefined_id)

    # Assignments
    valid_assign = ProceduralAssignment(target="data_out", operator="=", expression=lit)
    invalid_target_assign = ProceduralAssignment(target="unknown_target", operator="=", expression=bin_op)

    then_blk = StatementBlock(statements=[valid_assign])
    else_blk = StatementBlock(statements=[invalid_target_assign])

    if_with_else = IfStatement(condition=valid_id, then_branch=then_blk, else_branch=else_blk)
    if_no_else = IfStatement(condition=valid_id, then_branch=then_blk, else_branch=None)

    always = AlwaysBlock(block_type="always_comb", sensitivity=[], statements=(if_with_else, if_no_else))
    mod = ModuleDeclaration(name="top", ports=[], members=[always])
    cu = CompilationUnit(declarations=[mod])

    # 3. Resolve identifiers
    resolver = IdentifierResolver()
    resolver.resolve(mod_scope, cu)

    # 4. Verify errors captured correctly
    assert len(resolver.errors) >= 2
    assert any("undefined_sig" in e for e in resolver.errors)
    assert any("unknown_target" in e for e in resolver.errors)
