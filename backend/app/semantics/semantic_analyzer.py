"""
RIVA Semantic Analyzer.
"""

from app.compiler.pass_manager import PassManager

from app.diagnostics.diagnostic_engine import DiagnosticEngine

from app.semantics.semantic_model import SemanticModel

from app.semantics.visitors.scope_builder import ScopeBuilder
from app.semantics.evaluation.constant_evaluator import ConstantEvaluator
from app.semantics.type_checking.type_resolver import TypeResolver
from app.semantics.width.width_inference import WidthInference
from app.semantics.passes.signedness_resolver import SignednessResolver
from app.semantics.passes.identifier_checker import IdentifierChecker



class SemanticAnalyzer:

    def __init__(self):

        self.scope_builder = ScopeBuilder()

        self.constant_evaluator = ConstantEvaluator()

        self.type_resolver = TypeResolver()

        self.width_inference = WidthInference()

        self.signedness_resolver = SignednessResolver()

        self.identifier_checker = IdentifierChecker()

        self.diagnostic_engine = DiagnosticEngine()


        self.pass_manager = PassManager()

        self.pass_manager.register(
            self._scope_builder_pass,
        )

        self.pass_manager.register(
            self._constant_evaluator_pass,
        )

        self.pass_manager.register(
            self._type_resolver_pass,
        )

        self.pass_manager.register(
            self._width_inference_pass,
        )

        self.pass_manager.register(
            self._signedness_resolver_pass,
        )

        self.pass_manager.register(
            self._identifier_checker_pass,
        )


    def analyze(
        self,
        syntax_tree,
    ):

        model = SemanticModel()

        self.pass_manager.run(
            syntax_tree,
            model,
        )

        model.syntax_tree = syntax_tree

        self.diagnostic_engine.analyze(
            model,
        )

        return model

    def _scope_builder_pass(
        self,
        syntax_tree,
        model,
    ):

        model.scopes["global"] = (
            self.scope_builder.analyze(
                syntax_tree,
            )
        )

        model.diagnostics.extend(
            self.scope_builder.collector.diagnostics
        )

    def _constant_evaluator_pass(
        self,
        syntax_tree,
        model,
    ):

        self.constant_evaluator.evaluate(
            syntax_tree,
            model,
        )

    def _type_resolver_pass(
        self,
        syntax_tree,
        model,
    ):

        self.type_resolver.resolve(
            syntax_tree,
            model,
        )

    def _width_inference_pass(
        self,
        syntax_tree,
        model,
    ):

        self.width_inference.infer(
            syntax_tree,
            model,
        )

    def _signedness_resolver_pass(
        self,
        syntax_tree,
        model,
    ):

        self.signedness_resolver.resolve(
            syntax_tree,
            model,
        )

    def _identifier_checker_pass(
        self,
        syntax_tree,
        model,
    ):

        self.identifier_checker.check(
            syntax_tree,
            model,
        )

