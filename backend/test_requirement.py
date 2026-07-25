from app.domain.requirement import Requirement


req = Requirement(
    requirement_id="REQ_001",
    category="Functional",
    description="If sel is 0, output y shall equal a.",
    condition="sel == 0",
    expected_result="y = a"
)

print("\n===== Requirement =====\n")
print(req)
print("\nRequirement ID :", req.requirement_id)
print("Category       :", req.category)
print("Condition      :", req.condition)
print("Expected       :", req.expected_result)
