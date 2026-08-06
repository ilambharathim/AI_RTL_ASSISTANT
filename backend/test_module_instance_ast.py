from app.ast.module_instance import ModuleInstance

instance = ModuleInstance(

    module_name="adder",

    parameter_overrides=(),

    instance_name="u0",

    connections=(),

)

assert instance.kind == "ModuleInstance"

assert instance.module_name == "adder"

assert instance.parameter_overrides == ()

assert instance.instance_name == "u0"

assert instance.connections == ()

print("ModuleInstance AST test passed.")

