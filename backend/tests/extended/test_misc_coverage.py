"""
Comprehensive tests for miscellaneous modules with coverage gaps:
- config/settings.py (8 stmts, 0%)
- domain/rtl_tokens/token.py (3 missed)
- domain/rtl_ast/rtl_node.py (3 missed)
- domain/rtl_ast/module_node.py (3 missed)
- engines/rule_engine/validation_result.py (4 missed)
- engines/rule_engine/validation_rule.py (3 missed)
- parsers/rtl/parse_result.py (3 stmts, 0%)
- parsers/rtl/lexer_result.py (5 missed)
- parsers/rtl/character_stream.py (3 missed)
- preprocessors/rtl/handlers/ifndef_handler.py (3 missed)
- ai/evidence_store.py (3 missed)
- elaboration/cfg/cfg_elaborator.py (9 stmts, 0%)
"""

import pytest


# ── Config Settings ──────────────────────────────────────────────────

def test_settings_defaults():
    pydantic_settings = pytest.importorskip("pydantic_settings")
    from app.config.settings import Settings, settings
    s = Settings()
    assert s.PROJECT_NAME == "RIVA"
    assert s.VERSION == "1.0.0"
    assert s.API_PREFIX == "/api"
    assert settings.PROJECT_NAME == "RIVA"


# ── RTL Token Domain ────────────────────────────────────────────────

def test_rtl_token_valid():
    from app.domain.rtl_tokens.token import RTLToken
    from app.domain.rtl_tokens.token_type import RTLTokenType
    from app.shared.source_location import SourceLocation

    loc = SourceLocation(line=1, column=1)
    tok = RTLToken(token_type=RTLTokenType.IDENTIFIER, value="foo", source_location=loc)
    assert tok.value == "foo"


def test_rtl_token_invalid_type():
    from app.domain.rtl_tokens.token import RTLToken
    from app.shared.source_location import SourceLocation

    loc = SourceLocation(line=1, column=1)
    with pytest.raises(TypeError, match="token_type must be"):
        RTLToken(token_type="bad", value="foo", source_location=loc)


def test_rtl_token_invalid_value():
    from app.domain.rtl_tokens.token import RTLToken
    from app.domain.rtl_tokens.token_type import RTLTokenType
    from app.shared.source_location import SourceLocation

    loc = SourceLocation(line=1, column=1)
    with pytest.raises(TypeError, match="value must be a string"):
        RTLToken(token_type=RTLTokenType.IDENTIFIER, value=123, source_location=loc)


def test_rtl_token_invalid_location():
    from app.domain.rtl_tokens.token import RTLToken
    from app.domain.rtl_tokens.token_type import RTLTokenType

    with pytest.raises(TypeError, match="source_location must be"):
        RTLToken(token_type=RTLTokenType.IDENTIFIER, value="foo", source_location="bad")


# ── RTL Node Domain ─────────────────────────────────────────────────

def test_rtl_node_basic():
    from app.domain.rtl_ast.rtl_node import RTLNode
    from app.shared.source_location import SourceLocation

    node = RTLNode()
    assert node.child_count == 0
    assert node.iter_children() == ()

    child = RTLNode()
    node.add_child(child)
    assert node.child_count == 1


def test_rtl_node_invalid_source_location():
    from app.domain.rtl_ast.rtl_node import RTLNode

    with pytest.raises(TypeError, match="source_location must be"):
        RTLNode(source_location="bad")


def test_rtl_node_add_child_invalid():
    from app.domain.rtl_ast.rtl_node import RTLNode

    node = RTLNode()
    with pytest.raises(TypeError, match="child must be an RTLNode"):
        node.add_child("not_a_node")


# ── Module Node Domain ──────────────────────────────────────────────

def test_module_node_basic():
    from app.domain.rtl_ast.module_node import ModuleNode
    from app.domain.rtl_ast.rtl_node import RTLNode

    mod = ModuleNode(name="top")
    port = RTLNode()
    param = RTLNode()
    member = RTLNode()

    mod.add_port(port)
    mod.add_parameter(param)
    mod.add_member(member)

    assert len(mod.ports) == 1
    assert len(mod.parameters) == 1
    assert len(mod.members) == 1
    assert mod.child_count == 3


def test_module_node_invalid_port():
    from app.domain.rtl_ast.module_node import ModuleNode

    mod = ModuleNode(name="top")
    with pytest.raises(TypeError, match="port must be an RTLNode"):
        mod.add_port("not_a_node")


def test_module_node_invalid_parameter():
    from app.domain.rtl_ast.module_node import ModuleNode

    mod = ModuleNode(name="top")
    with pytest.raises(TypeError, match="parameter must be an RTLNode"):
        mod.add_parameter("not_a_node")


def test_module_node_invalid_member():
    from app.domain.rtl_ast.module_node import ModuleNode

    mod = ModuleNode(name="top")
    with pytest.raises(TypeError, match="member must be an RTLNode"):
        mod.add_member("not_a_node")


# ── Validation Result ────────────────────────────────────────────────

def test_validation_result_valid():
    from app.engines.rule_engine.validation_result import ValidationRuleResult

    result = ValidationRuleResult(rule_id="R001")
    assert result.diagnostic_count == 0
    assert result.error_count == 0
    assert result.warning_count == 0
    assert result.info_count == 0
    assert result.is_successful
    assert not result.has_errors


def test_validation_result_with_diagnostics():
    from app.engines.rule_engine.validation_result import ValidationRuleResult
    from app.engines.diagnostics.diagnostic import Diagnostic
    from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity

    d = Diagnostic(code="R001", message="test error", severity=DiagnosticSeverity.ERROR, stage="test")
    result = ValidationRuleResult(rule_id="R001", diagnostics=(d,))
    assert result.diagnostic_count == 1
    assert result.error_count == 1
    assert result.has_errors
    assert not result.is_successful


def test_validation_result_invalid_rule_id():
    from app.engines.rule_engine.validation_result import ValidationRuleResult

    with pytest.raises(TypeError, match="rule_id must be a string"):
        ValidationRuleResult(rule_id=123)

    with pytest.raises(ValueError, match="rule_id must not be empty"):
        ValidationRuleResult(rule_id="  ")


def test_validation_result_invalid_diagnostics():
    from app.engines.rule_engine.validation_result import ValidationRuleResult

    with pytest.raises(TypeError, match="diagnostics must be a tuple"):
        ValidationRuleResult(rule_id="R001", diagnostics=[])

    with pytest.raises(TypeError, match="diagnostics must contain only"):
        ValidationRuleResult(rule_id="R001", diagnostics=("not_diagnostic",))


# ── Validation Rule ──────────────────────────────────────────────────

def test_validation_rule_run():
    from app.engines.rule_engine.validation_rule import ValidationRule
    from app.domain.specification_ir import SpecificationIR

    class GoodRule(ValidationRule):
        rule_id = "TEST001"
        description = "Test rule"
        stage = "specification-validation"

        def _evaluate(self, specification):
            return ()

    rule = GoodRule()
    spec = SpecificationIR()
    result = rule.run(spec)
    assert result.rule_id == "TEST001"
    assert result.diagnostic_count == 0


def test_validation_rule_invalid_spec():
    from app.engines.rule_engine.validation_rule import ValidationRule

    class GoodRule(ValidationRule):
        rule_id = "TEST002"
        description = "Test rule"
        stage = "specification-validation"

        def _evaluate(self, specification):
            return ()

    rule = GoodRule()
    with pytest.raises(TypeError, match="specification must be"):
        rule.run("not_a_spec")


def test_validation_rule_bad_return_type():
    from app.engines.rule_engine.validation_rule import ValidationRule
    from app.domain.specification_ir import SpecificationIR

    class BadReturnRule(ValidationRule):
        rule_id = "TEST003"
        description = "Test rule"
        stage = "specification-validation"

        def _evaluate(self, specification):
            return []  # should be tuple

    rule = BadReturnRule()
    with pytest.raises(TypeError, match="must return a tuple"):
        rule.run(SpecificationIR())


def test_validation_rule_subclass_validation():
    from app.engines.rule_engine.validation_rule import ValidationRule

    with pytest.raises(TypeError, match="non-empty string rule_id"):
        class NoRuleId(ValidationRule):
            description = "Test"
            def _evaluate(self, spec): return ()


# ── Parse Result ─────────────────────────────────────────────────────

def test_parse_result_compatibility():
    from app.parsers.rtl.parse_result import RTLParseResult
    from app.parsers.rtl.parser_result import RTLParserResult
    assert RTLParseResult is RTLParserResult


# ── Lexer Result ─────────────────────────────────────────────────────

def test_lexer_result_basic():
    from app.parsers.rtl.lexer_result import RTLLexerResult
    result = RTLLexerResult(tokens=(), diagnostics=())
    assert result.successful
    assert not result.has_errors
    assert not result.has_warnings


def test_lexer_result_invalid_tokens():
    from app.parsers.rtl.lexer_result import RTLLexerResult
    with pytest.raises(TypeError, match="tokens must be a tuple"):
        RTLLexerResult(tokens=[], diagnostics=())


def test_lexer_result_invalid_token_contents():
    from app.parsers.rtl.lexer_result import RTLLexerResult
    with pytest.raises(TypeError, match="tokens must contain only"):
        RTLLexerResult(tokens=("not_a_token",), diagnostics=())


def test_lexer_result_invalid_diagnostics():
    from app.parsers.rtl.lexer_result import RTLLexerResult
    with pytest.raises(TypeError, match="diagnostics must be a tuple"):
        RTLLexerResult(tokens=(), diagnostics=[])


def test_lexer_result_invalid_diagnostic_contents():
    from app.parsers.rtl.lexer_result import RTLLexerResult
    with pytest.raises(TypeError, match="diagnostics must contain only"):
        RTLLexerResult(tokens=(), diagnostics=("not_diag",))


def test_lexer_result_with_errors():
    from app.parsers.rtl.lexer_result import RTLLexerResult
    from app.engines.diagnostics.diagnostic import Diagnostic
    from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity

    err = Diagnostic(code="E001", message="error", severity=DiagnosticSeverity.ERROR, stage="lex")
    warn = Diagnostic(code="W001", message="warn", severity=DiagnosticSeverity.WARNING, stage="lex")
    result = RTLLexerResult(tokens=(), diagnostics=(err, warn))
    assert result.has_errors
    assert result.has_warnings
    assert not result.successful


# ── Character Stream ─────────────────────────────────────────────────

def test_character_stream_basic():
    from app.parsers.rtl.character_stream import CharacterStream

    stream = CharacterStream(source="ab\nc")
    assert not stream.eof()
    assert stream.peek() == "a"
    assert stream.advance() == "a"
    assert stream.advance() == "b"
    assert stream.advance() == "\n"  # line advances
    assert stream.line == 2
    assert stream.column == 1
    assert stream.advance() == "c"
    assert stream.eof()
    assert stream.peek() == ""
    assert stream.advance() == ""

    loc = stream.location()
    assert loc.line == 2


def test_character_stream_invalid_source():
    from app.parsers.rtl.character_stream import CharacterStream

    with pytest.raises(TypeError, match="source must be a string"):
        CharacterStream(source=123)


# ── Ifndef Handler ───────────────────────────────────────────────────

def test_ifndef_handler_matches():
    from app.preprocessors.rtl.handlers.ifndef_handler import IfndefHandler

    assert IfndefHandler.matches("`ifndef GUARD")
    assert not IfndefHandler.matches("`ifdef GUARD")


def test_ifndef_handler_handle():
    from app.preprocessors.rtl.handlers.ifndef_handler import IfndefHandler
    from app.preprocessors.rtl.macro_table import MacroTable

    mt = MacroTable()
    stack = [True]

    # macro not defined → enabled
    result = IfndefHandler.handle("`ifndef GUARD", mt, stack)
    assert result is True
    assert stack[-1] is True

    # macro defined → disabled
    mt.define("GUARD", "1")
    stack2 = [True]
    IfndefHandler.handle("`ifndef GUARD", mt, stack2)
    assert stack2[-1] is False


# ── Evidence Store ───────────────────────────────────────────────────

def test_evidence_store_all_methods():
    from app.ai.evidence_store import EvidenceStore
    from app.simulation.simulation_adapter import SimulationResult

    store = EvidenceStore("test_project")
    store.add_diagnostics([])
    store.add_traceability_links([])

    sim = SimulationResult(
        status="pass",
        exit_code=0,
        simulator_name="iverilog",
        errors_count=0,
        warnings_count=0,
    )
    store.add_simulation_result(sim)
    store.add_waveform_observations([])
    store.set_hierarchy_summary({"modules": 1})
    store.add_knowledge_context("test context")

    payload = store.get_payload()
    assert payload.project_name == "test_project"
    d = payload.to_dict()
    assert d["project_name"] == "test_project"
    assert d["hierarchy"] == {"modules": 1}
    assert "test context" in d["knowledge"]


# ── CFG Elaborator ───────────────────────────────────────────────────

def test_cfg_elaborator_basic():
    from app.elaboration.cfg.cfg_elaborator import CFGElaborator
    from app.semantics.semantic_model import SemanticModel
    from app.elaboration.model.elaboration_model import ElaborationModel
    from app.ast import CompilationUnit, ModuleDeclaration, AlwaysBlock, ProceduralAssignment
    from app.ast.expression import LiteralExpression

    class MockElaborationModel(ElaborationModel):
        __slots__ = ("cfgs",)

    model = SemanticModel()
    model.elaboration = MockElaborationModel()

    assign = ProceduralAssignment(target="a", operator="=", expression=LiteralExpression("1"))
    always = AlwaysBlock(block_type="always_comb", sensitivity=[], statements=[assign])
    mod = ModuleDeclaration(name="top", ports=[], members=[always])

    model.elaboration.elaborated_modules = {"top": mod}

    elab = CFGElaborator()
    elab.elaborate(model)

    assert "top" in model.elaboration.cfgs
