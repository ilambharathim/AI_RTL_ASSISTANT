from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser


def parse_rtl(source):
    lexer_result = RTLLexer().tokenize(source)

    parser_result = RTLParser().parse(
        lexer_result.tokens,
    )

    return parser_result.syntax_tree


def get_member(module, name):
    members = [
        member
        for member in module.members
        if member.__class__.__name__ == name
    ]

    assert len(members) == 1
    return members[0]


def test_generate_for_with_multiple_module_instances():
    source = """
module test;

generate
    for (genvar i = 0; i < 2; i = i + 1) begin : gen_loop

        child_a u_a (
            .a(i)
        );

        child_b u_b (
            .b(i)
        );

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate = get_member(module, "GenerateFor")

    assert len(generate.members) == 2

    assert generate.members[0].__class__.__name__ == "ModuleInstance"
    assert generate.members[1].__class__.__name__ == "ModuleInstance"


def test_nested_generate_if_inside_generate_for():
    source = """
module test;

generate
    for (genvar i = 0; i < 2; i = i + 1) begin : gen_loop

        if (ENABLE) begin : gen_enabled

            child u_child (
                .a(i)
            );

        end

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate_for = get_member(module, "GenerateFor")

    assert len(generate_for.members) == 1

    generate_if = generate_for.members[0]

    assert generate_if.__class__.__name__ == "GenerateIf"
    assert generate_if.condition.name == "ENABLE"
    assert len(generate_if.true_members) == 1
    assert generate_if.true_members[0].__class__.__name__ == "ModuleInstance"


def test_nested_generate_for_inside_generate_if():
    source = """
module test;

generate
    if (ENABLE) begin : gen_enabled

        for (genvar i = 0; i < 2; i = i + 1) begin : gen_loop

            child u_child (
                .a(i)
            );

        end

    end
endgenerate

endmodule
"""

    tree = parse_rtl(source)

    module = tree.declarations[0]
    generate_if = get_member(module, "GenerateIf")

    assert len(generate_if.true_members) == 1

    generate_for = generate_if.true_members[0]

    assert generate_for.__class__.__name__ == "GenerateFor"
    assert generate_for.variable == "i"
    assert len(generate_for.members) == 1
    assert generate_for.members[0].__class__.__name__ == "ModuleInstance"
