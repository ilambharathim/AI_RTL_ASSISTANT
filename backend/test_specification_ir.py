from app.domain.metadata import Metadata
from app.domain.port import Port
from app.domain.requirement import Requirement
from app.domain.specification_ir import SpecificationIR


metadata = Metadata(
    project_name="RIVA",
    module_name="mux2to1",
    description="2-to-1 Multiplexer",
    language="SystemVerilog"
)

port_a = Port(
    name="a",
    direction="input"
)

port_b = Port(
    name="b",
    direction="input"
)

port_sel = Port(
    name="sel",
    direction="input"
)

port_y = Port(
    name="y",
    direction="output"
)

req = Requirement(
    requirement_id="REQ_001",
    category="Functional",
    description="Output follows selected input.",
    condition="sel == 0",
    expected_result="y = a"
)

spec = SpecificationIR(
    metadata=metadata,
    ports=[port_a, port_b, port_sel, port_y],
    requirements=[req]
)

print("\n========== Specification IR ==========\n")
print(spec)

print("\nModule :", spec.metadata.module_name)
print("Ports  :", len(spec.ports))
print("Requirements :", len(spec.requirements))
