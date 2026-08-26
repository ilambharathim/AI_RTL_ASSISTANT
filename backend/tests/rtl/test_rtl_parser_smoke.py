from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def test_rtl_parser_smoke():

    source = """
    module test (
        input logic clk,
        output logic [7:0] data
    );

    logic [7:0] a;

    assign data = a;

    endmodule
    """

    lexer_result = RTLLexer().tokenize(source)

    assert lexer_result.successful
    assert not lexer_result.diagnostics

    parser_result = RTLParser().parse(
        lexer_result.tokens
    )

    assert parser_result.successful
    assert not parser_result.diagnostics

    # ============================================================
    # LEGACY AST
    # ============================================================

    tree = parser_result.syntax_tree

    assert tree is not None
    assert len(tree.declarations) == 1

    module = tree.declarations[0]

    assert module.name == "test"
    assert len(module.ports) == 2
    assert len(module.members) == 2

    clk = module.ports[0]
    data = module.ports[1]

    assert clk.name == "clk"
    assert clk.direction == "input"
    assert clk.signal_type == "logic"
    assert clk.packed_range is None

    assert data.name == "data"
    assert data.direction == "output"
    assert data.signal_type == "logic"
    assert data.packed_range is not None

    signal = module.members[0]
    assignment = module.members[1]

    assert signal.name == "a"
    assert assignment.target == "data"
    assert assignment.expression == "a"

    # ============================================================
    # NEW RTL AST
    # ============================================================

    new_tree = parser_result.rtl_ast

    assert new_tree is not None
    assert new_tree.module_count == 1

    new_module = new_tree.modules[0]

    assert new_module.name == "test"
    assert len(new_module.ports) == 2
    assert len(new_module.members) == 2
    assert new_module.child_count == 4

    new_clk = new_module.ports[0]
    new_data = new_module.ports[1]

    assert new_clk.name == "clk"
    assert new_clk.direction == "input"
    assert new_clk.datatype == "logic"
    assert new_clk.width == 1

    assert new_data.name == "data"
    assert new_data.direction == "output"
    assert new_data.datatype == "logic"
    assert new_data.width == 8

    new_signal = new_module.members[0]
    new_assign = new_module.members[1]

    assert new_signal.name == "a"
    assert new_signal.datatype == "logic"
    assert new_signal.width == 8

    assert new_assign.target == "data"
    assert new_assign.expression == "a"
