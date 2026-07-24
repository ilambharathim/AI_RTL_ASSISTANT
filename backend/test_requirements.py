"""
Test the Specification Reader and Parser.
"""

from pathlib import Path

from app.modules.specification.reader import SpecificationReader
from app.modules.specification.parser import SpecificationParser


# -----------------------------------------------------
# Locate Project Root
# -----------------------------------------------------

CURRENT_FILE = Path(__file__).resolve()

BACKEND_DIR = CURRENT_FILE.parent

PROJECT_ROOT = BACKEND_DIR.parent

SPEC_PATH = PROJECT_ROOT / "examples" / "specification.txt"


# -----------------------------------------------------
# Read Specification
# -----------------------------------------------------

reader = SpecificationReader()

text = reader.read(str(SPEC_PATH))


# -----------------------------------------------------
# Parse Specification
# -----------------------------------------------------

parser = SpecificationParser()

spec = parser.parse(text)


# -----------------------------------------------------
# Display Results
# -----------------------------------------------------

print("\n========== Parsed Specification ==========\n")

print("Module Name")
print(spec.module_name)

print("\nInputs")
print(spec.inputs)

print("\nOutputs")
print(spec.outputs)

print("\nFunctional Requirements")

for rule in spec.requirements:

    print("----------------------------")
    print("Condition :", rule.condition)
    print("Output    :", rule.output_signal)
    print("Expected  :", rule.expected_value)

print("\n==========================================")