from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source):
    lexer_result = RTLLexer().tokenize(source)

    parser_result = RTLParser().parse(
        lexer_result.tokens,
    )

    return parser_result.syntax_tree


def get_generate_if(module):
    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateIf"
    ]

    assert len(generates) == 1

    return generates[0]


def test_generate_if_basic():
    source = """
module test;

generate
    if (1) begin : gen_enabled
    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generate = get_generate_if(module)

    assert generate.condition.value == "1"
    assert len(generate.true_members) == 0
    assert len(generate.false_members) == 0


def test_generate_if_with_signal_condition():
    source = """
module test;

parameter ENABLE = 1;

generate
    if (ENABLE) begin : gen_enabled
    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generate = get_generate_if(module)

    assert generate.condition.name == "ENABLE"


def test_generate_if_else():
    source = """
module test;

parameter ENABLE = 1;

generate
    if (ENABLE) begin : gen_enabled
    end
    else begin : gen_disabled
    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generate = get_generate_if(module)

    assert generate.condition.name == "ENABLE"
    assert len(generate.true_members) == 0
    assert len(generate.false_members) == 0


def test_generate_if_without_explicit_generate():
    source = """
module test;

if (1) begin : gen_enabled
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generate = get_generate_if(module)

    assert generate.condition.value == "1"
