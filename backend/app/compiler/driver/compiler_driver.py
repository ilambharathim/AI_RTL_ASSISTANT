"""
RIVA Compiler Driver.

Coordinates the complete compilation pipeline.
"""

from app.parsers.rtl.parser import RTLParser

from app.semantics.semantic_analyzer import (
    SemanticAnalyzer,
)

from app.elaboration.elaborator import Elaborator

from app.optimization.optimizer import Optimizer

from app.diagnostics.diagnostic_engine import (
    DiagnosticEngine,
)

from app.repair.repair_engine import (
    RepairEngine,
)

from app.repair.patches.patch_generator import (
    PatchGenerator,
)


class CompilerDriver:

    def compile(
        self,
        tokens,
    ):

        parse_result = RTLParser().parse(
            tokens,
        )

        syntax_tree = (
            parse_result.syntax_tree
        )

        semantic_model = (
            SemanticAnalyzer().analyze(
                syntax_tree,
            )
        )

        Elaborator().elaborate(
            syntax_tree,
            semantic_model,
        )

        Optimizer().optimize(
            semantic_model,
        )

        DiagnosticEngine().analyze(
            semantic_model,
        )

        RepairEngine().generate(
            semantic_model,
        )

        PatchGenerator().generate(
            semantic_model,
        )

        return semantic_model
