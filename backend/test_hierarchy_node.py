from app.elaboration.hierarchy_node import HierarchyNode

node = HierarchyNode(
    name="u0",
    module_name="adder",
)

assert node.name == "u0"
assert node.module_name == "adder"
assert node.children == []

print("HierarchyNode test passed.")
