from app.ast import (
    CompilationUnit,
    SignalDeclaration,
)

from app.semantics.semantic_analyzer import SemanticAnalyzer

tree = CompilationUnit(

    declarations=(

        SignalDeclaration(

            signal_type="logic",

            packed_range=None,

            name="clk",

        ),

    ),

)

model = SemanticAnalyzer().analyze(tree)

assert model.symbols["clk"].width == 1

print("WidthInference test passed.")

