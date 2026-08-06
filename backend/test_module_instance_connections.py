from app.ast.module_instance import ModuleInstance

node = ModuleInstance(

    module_name="adder",

    parameter_overrides=(),

    instance_name="u0",

    connections=(),

)

assert node.module_name == "adder"

assert node.parameter_overrides == ()

assert node.instance_name == "u0"

assert node.connections == ()

print("ModuleInstance connections test passed.")

