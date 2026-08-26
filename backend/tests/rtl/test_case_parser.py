from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source):
    lexer_result = RTLLexer().tokenize(source)

    parser_result = RTLParser().parse(
        lexer_result.tokens,
    )

    return parser_result.syntax_tree


def get_always_block(module):
    blocks = [
        member
        for member in module.members
        if member.__class__.__name__ == "AlwaysBlock"
    ]

    assert len(blocks) == 1

    return blocks[0]


def test_case_statement():
    source = """
module test(
    input logic [1:0] sel,
    input logic a,
    input logic b,
    output logic y
);

always_comb begin
    case (sel)
        2'b00: y = a;
        2'b01: y = b;
        default: y = 1'b0;
    endcase
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_block = get_always_block(module)

    assert len(always_block.statements) == 1

    case_statement = always_block.statements[0]

    assert case_statement.__class__.__name__ == "CaseStatement"
    assert case_statement.expression == "sel"
    assert len(case_statement.items) == 3


def test_casez_statement():
    source = """
module test(
    input logic [3:0] sel,
    output logic y
);

always_comb begin
    casez (sel)
        4'b1???: y = 1'b1;
        default: y = 1'b0;
    endcase
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_block = get_always_block(module)

    assert len(always_block.statements) == 1

    case_statement = always_block.statements[0]

    assert case_statement.__class__.__name__ == "CaseStatement"


def test_casex_statement():
    source = """
module test(
    input logic [3:0] sel,
    output logic y
);

always_comb begin
    casex (sel)
        4'b1xxx: y = 1'b1;
        default: y = 1'b0;
    endcase
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_block = get_always_block(module)

    assert len(always_block.statements) == 1

    case_statement = always_block.statements[0]

    assert case_statement.__class__.__name__ == "CaseStatement"


def test_case_multiple_statements():
    source = """
module test(
    input logic [1:0] sel,
    input logic a,
    output logic y
);

always_comb begin
    case (sel)
        2'b00: begin
            y = a;
            y = 1'b0;
        end

        default: begin
            y = 1'b1;
        end
    endcase
end

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]

    always_block = get_always_block(module)

    assert len(always_block.statements) == 1

    case_statement = always_block.statements[0]

    assert case_statement.__class__.__name__ == "CaseStatement"
    assert len(case_statement.items) == 2
