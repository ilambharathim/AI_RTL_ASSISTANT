from app.domain.ast.document_node import DocumentNode
from app.domain.ast.section_node import SectionNode
from app.domain.ast.keyvalue_node import KeyValueNode
from app.domain.ast.listitem_node import ListItemNode

doc = DocumentNode()

doc.title = "RIVA Specification"

metadata = SectionNode("Metadata")
ports = SectionNode("Inputs")

metadata.add_entry(KeyValueNode("Module Name", "mux2to1"))

ports.add_entry(ListItemNode("a"))
ports.add_entry(ListItemNode("b"))
ports.add_entry(ListItemNode("sel"))

doc.add_section(metadata)
doc.add_section(ports)

print("\n========== DOCUMENT AST ==========\n")

print("Title :", doc.title)

print("Children :", doc.child_count())

print()

for section in doc.sections:

    print(f"Section : {section.name}")

    for item in section.entries:

        print("   ", item)

    print()
