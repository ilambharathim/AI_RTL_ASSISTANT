from app.modules.specification.specification_service import SpecificationService

service = SpecificationService()

spec = service.load("../examples/specification.txt")

print()

print("Module :", spec.module_name)

print("Inputs :", spec.inputs)

print("Outputs:", spec.outputs)