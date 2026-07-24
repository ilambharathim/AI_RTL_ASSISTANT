from app.modules.specification.specification_service import SpecificationService


service = SpecificationService()

content = service.load("../examples/specification.txt")

print(content)