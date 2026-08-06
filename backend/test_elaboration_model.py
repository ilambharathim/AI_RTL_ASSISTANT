from app.semantics.semantic_model import SemanticModel

model = SemanticModel()

model.elaboration.hierarchy["top"] = []

assert "top" in model.elaboration.hierarchy

print("ElaborationModel test passed.")

