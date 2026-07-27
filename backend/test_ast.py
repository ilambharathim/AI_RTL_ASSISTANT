"""
Regression tests for the RIVA generic specification AST.
"""

from app.domain.specification_ast.ast_node import ASTNode
from app.domain.specification_ast.document_node import DocumentNode
from app.domain.specification_ast.keyvalue_node import KeyValueNode
from app.domain.specification_ast.listitem_node import ListItemNode
from app.domain.specification_ast.section_node import SectionNode
from app.domain.specification_ast.text_node import TextNode


def assert_raises(
    expected_exception: type[Exception],
    expected_message: str,
    operation,
) -> None:
    try:
        operation()
    except expected_exception as error:
        assert str(error) == expected_message
    else:
        raise AssertionError(
            f"Expected {expected_exception.__name__}: {expected_message}"
        )


def test_complete_document_structure() -> None:
    document = DocumentNode(
        title="RIVA Specification",
        line=1,
        column=1,
        source_file="mux_spec.txt",
    )

    metadata = KeyValueNode(
        "Module Name",
        "mux2to1",
        line=1,
        column=1,
        source_file="mux_spec.txt",
    )
    inputs = SectionNode(
        "Inputs",
        line=2,
        column=1,
        source_file="mux_spec.txt",
    )
    clock = ListItemNode(
        "clk",
        line=3,
        column=1,
        source_file="mux_spec.txt",
    )
    behavior = TextNode(
        "The output shall update combinationally.",
        line=4,
        column=1,
        source_file="mux_spec.txt",
    )

    document.add_entry(metadata)
    inputs.add_entry(clock)
    inputs.add_entry(behavior)
    document.add_section(inputs)

    assert document.node_type == "DOCUMENT"
    assert document.title == "RIVA Specification"
    assert document.line == 1
    assert document.column == 1
    assert document.source_file == "mux_spec.txt"

    assert document.entries == [metadata]
    assert document.sections == [inputs]
    assert document.children == [metadata, inputs]
    assert document.child_count() == 2

    assert inputs.entries == [clock, behavior]
    assert inputs.children == [clock, behavior]
    assert inputs.child_count() == 2


def test_mutable_collections_are_not_shared() -> None:
    first_document = DocumentNode()
    second_document = DocumentNode()

    first_section = SectionNode("Inputs")
    second_section = SectionNode("Outputs")

    first_document.add_section(first_section)
    second_document.add_section(second_section)

    assert first_document.children is not second_document.children
    assert first_document.sections is not second_document.sections
    assert first_section.entries is not second_section.entries


def test_node_validation() -> None:
    assert_raises(
        ValueError,
        "node_type must be a non-empty string.",
        lambda: ASTNode(""),
    )
    assert_raises(
        ValueError,
        "line must be an integer greater than or equal to 0.",
        lambda: ASTNode("TEST", line=-1),
    )
    assert_raises(
        ValueError,
        "column must be an integer greater than or equal to 0.",
        lambda: ASTNode("TEST", column=-1),
    )
    assert_raises(
        TypeError,
        "source_file must be a string.",
        lambda: ASTNode("TEST", source_file=123),
    )
    assert_raises(
        TypeError,
        "child must be an ASTNode.",
        lambda: ASTNode("TEST").add_child("invalid"),
    )


def test_document_validation() -> None:
    document = DocumentNode()

    assert_raises(
        TypeError,
        "title must be a string.",
        lambda: DocumentNode(title=123),
    )
    assert_raises(
        TypeError,
        "entry must be an ASTNode.",
        lambda: document.add_entry("invalid"),
    )
    assert_raises(
        TypeError,
        "section nodes must be added with add_section().",
        lambda: document.add_entry(SectionNode("Inputs")),
    )
    assert_raises(
        TypeError,
        "section must be a SectionNode.",
        lambda: document.add_section(TextNode("invalid")),
    )


def test_section_validation() -> None:
    section = SectionNode("Inputs")

    assert_raises(
        TypeError,
        "name must be a string.",
        lambda: SectionNode(123),
    )
    assert_raises(
        ValueError,
        "name must not be empty.",
        lambda: SectionNode("   "),
    )
    assert_raises(
        TypeError,
        "entry must be an ASTNode.",
        lambda: section.add_entry("invalid"),
    )
    assert_raises(
        TypeError,
        "nested sections are not supported by this AST.",
        lambda: section.add_entry(SectionNode("Nested")),
    )


def test_entry_validation() -> None:
    assert KeyValueNode("Description", "").value == ""

    assert_raises(
        TypeError,
        "key must be a string.",
        lambda: KeyValueNode(123, "value"),
    )
    assert_raises(
        ValueError,
        "key must not be empty.",
        lambda: KeyValueNode("   ", "value"),
    )
    assert_raises(
        TypeError,
        "value must be a string.",
        lambda: KeyValueNode("Key", 123),
    )
    assert_raises(
        ValueError,
        "value must not be empty.",
        lambda: ListItemNode("   "),
    )
    assert_raises(
        ValueError,
        "value must not be empty.",
        lambda: TextNode("   "),
    )


def main() -> None:
    tests = (
        test_complete_document_structure,
        test_mutable_collections_are_not_shared,
        test_node_validation,
        test_document_validation,
        test_section_validation,
        test_entry_validation,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nGeneric AST tests passed.")


if __name__ == "__main__":
    main()
