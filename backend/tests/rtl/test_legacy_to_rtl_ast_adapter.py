from app.parsers.rtl.adapters import LegacyToRTLASTAdapter
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source: str):
    lexer_result = RTLLexer().tokenize(source)

    assert lexer_result.successful
    assert not lexer_result.diagnostics

    parser_result = RTLParser().parse(
        lexer_result.tokens
    )

    assert parser_result.successful
    assert not parser_result.diagnostics
    assert parser_result.rtl_ast is not None

    return parser_result.rtl_ast


def test_adapter_converts_parameter_signal_and_assign():
    source = """
module test (
    input logic clk,
    output logic [7:0] data
);

parameter WIDTH = 8;

logic [7:0] a;

assign data = a;

endmodule
"""

    tree = parse_rtl(source)

    assert tree.module_count == 1

    module = tree.modules[0]

    assert module.name == "test"

    assert len(module.ports) == 2
    assert len(module.parameters) == 1
    assert len(module.members) == 2

    parameter = module.parameters[0]

    assert parameter.name == "WIDTH"
    assert parameter.value == "8"

    signal = module.members[0]

    assert signal.name == "a"
    assert signal.datatype == "logic"
    assert signal.width == 8

    assignment = module.members[1]

    assert assignment.target == "data"
    assert assignment.expression == "a"


def test_adapter_converts_module_instance():
    source = """
module child (
    input logic a,
    output logic y
);

endmodule

module top (
    input logic a,
    output logic y
);

child u_child (
    .a(a),
    .y(y)
);

endmodule
"""

    tree = parse_rtl(source)

    assert tree.module_count == 2

    top = tree.modules[1]

    instances = [
        member
        for member in top.members
        if member.__class__.__name__ == "InstanceNode"
    ]

    assert len(instances) == 1

    instance = instances[0]

    assert instance.module_name == "child"
    assert instance.instance_name == "u_child"


def test_adapter_converts_always_block():
    source = """
module test (
    input logic clk,
    input logic d,
    output logic q
);

always_ff @(posedge clk) begin
    q <= d;
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.modules[0]

    always_blocks = [
        member
        for member in module.members
        if member.__class__.__name__ == "AlwaysBlockNode"
    ]

    assert len(always_blocks) == 1

    always_block = always_blocks[0]

    assert always_block.block_type == "always_ff"
    assert "posedge clk" in always_block.sensitivity
    assert len(always_block.statements) == 1


def test_adapter_converts_generate_if():
    source = """
module test;

generate
    if (1) begin : gen_enabled
    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.modules[0]

    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateNode"
    ]

    assert len(generates) == 1

    generate = generates[0]

    assert generate.generate_type == "if"
    assert generate.condition == "1"
