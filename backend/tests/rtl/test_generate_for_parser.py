from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source):
    lexer_result = RTLLexer().tokenize(source)

    parser_result = RTLParser().parse(
        lexer_result.tokens,
    )

    return parser_result.syntax_tree


def test_generate_for_basic():
    source = """
module test;

generate
    for (genvar i = 0; i < 4; i = i + 1) begin : gen_loop
    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateFor"
    ]

    assert len(generates) == 1

    generate = generates[0]

    assert generate.variable == "i"


def test_generate_for_with_parameter():
    source = """
module test;

parameter WIDTH = 8;

generate
    for (genvar i = 0; i < WIDTH; i = i + 1) begin : gen_loop
    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateFor"
    ]

    assert len(generates) == 1

    generate = generates[0]

    assert generate.variable == "i"


def test_generate_for_without_explicit_generate():
    source = """
module test;

for (genvar i = 0; i < 2; i = i + 1) begin : gen_loop
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateFor"
    ]

    assert len(generates) == 1
