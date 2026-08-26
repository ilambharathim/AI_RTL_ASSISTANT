from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source):
    lexer_result = RTLLexer().tokenize(source)

    parser_result = RTLParser().parse(
        lexer_result.tokens,
    )

    return parser_result.syntax_tree


def get_generate_for(module):
    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateFor"
    ]

    assert len(generates) == 1
    return generates[0]


def get_generate_if(module):
    generates = [
        member
        for member in module.members
        if member.__class__.__name__ == "GenerateIf"
    ]

    assert len(generates) == 1
    return generates[0]


def test_generate_for_preserves_module_instance():
    source = """
module test;

generate
    for (genvar i = 0; i < 2; i = i + 1) begin : gen_loop

        child u_child (
            .a(i)
        );

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate = get_generate_for(module)

    assert generate.variable == "i"
    assert len(generate.members) == 1

    child = generate.members[0]

    assert child.__class__.__name__ == "ModuleInstance"


def test_generate_if_preserves_module_instance():
    source = """
module test;

generate
    if (ENABLE) begin : gen_enabled

        child u_child (
            .a(signal)
        );

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate = get_generate_if(module)

    assert generate.condition.name == "ENABLE"
    assert len(generate.true_members) == 1

    child = generate.true_members[0]

    assert child.__class__.__name__ == "ModuleInstance"


def test_generate_if_else_preserves_both_members():
    source = """
module test;

generate
    if (ENABLE) begin : gen_enabled

        child u_enabled (
            .a(signal)
        );

    end
    else begin : gen_disabled

        child u_disabled (
            .a(signal)
        );

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate = get_generate_if(module)

    assert len(generate.true_members) == 1
    assert len(generate.false_members) == 1

    assert generate.true_members[0].__class__.__name__ == "ModuleInstance"
    assert generate.false_members[0].__class__.__name__ == "ModuleInstance"
