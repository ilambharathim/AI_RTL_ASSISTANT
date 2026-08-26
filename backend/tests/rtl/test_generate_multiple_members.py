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


def test_generate_if_preserves_multiple_module_instances():
    source = """
module test;

generate
    if (ENABLE) begin : gen_enabled

        child u_first (
            .a(signal_a)
        );

        child u_second (
            .a(signal_b)
        );

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate = get_generate_if(module)

    assert len(generate.true_members) == 2

    first = generate.true_members[0]
    second = generate.true_members[1]

    assert first.__class__.__name__ == "ModuleInstance"
    assert second.__class__.__name__ == "ModuleInstance"

    assert first.instance_name == "u_first"
    assert second.instance_name == "u_second"
