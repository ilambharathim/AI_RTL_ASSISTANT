from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source):
    lexer_result = RTLLexer().tokenize(source)

    parser_result = RTLParser().parse(
        lexer_result.tokens,
    )

    return parser_result.syntax_tree


def test_if_else_with_nonblocking_assignment():
    source = """
module test(
    input logic clk,
    input logic a,
    input logic b,
    output logic q
);

always_ff @(posedge clk) begin
    if (a) begin
        q <= b;
    end else begin
        q <= a;
    end
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_blocks = [
        member
        for member in module.members
        if member.__class__.__name__ == "AlwaysBlock"
    ]

    assert len(always_blocks) == 1


def test_blocking_assignment_expression():
    source = """
module test(
    input logic a,
    input logic b,
    output logic q
);

always_comb begin
    q = a + b;
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_blocks = [
        member
        for member in module.members
        if member.__class__.__name__ == "AlwaysBlock"
    ]

    assert len(always_blocks) == 1


def test_nested_begin_end():
    source = """
module test(
    input logic a,
    output logic q
);

always_comb begin
    begin
        q = a;
    end
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_blocks = [
        member
        for member in module.members
        if member.__class__.__name__ == "AlwaysBlock"
    ]

    assert len(always_blocks) == 1
