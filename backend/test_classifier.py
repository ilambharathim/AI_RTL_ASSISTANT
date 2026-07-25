from app.parsers.specification.classifier import (
    DocumentClassifier,
)

tests = [

    "",

    "Inputs:",

    "Module Name: mux2to1",

    "clk",

    "This module implements a multiplexer.",

]

print("\n===== CLASSIFIER TEST =====\n")

for line in tests:

    token = DocumentClassifier.classify(line)

    print(f"{line!r:40} -> {token.name}")
