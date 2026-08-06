"""
RIVA Semantic Model.
"""

from dataclasses import dataclass, field

from app.elaboration.model import ElaborationModel
from app.optimization.model.optimization_context import (
    OptimizationContext,
)


@dataclass(slots=True)
class SemanticModel:
    """
    Central semantic repository.

    Stores semantic information produced by semantic analysis,
    elaboration, and optimization.
    """

    scopes: dict = field(default_factory=dict)

    symbols: dict = field(default_factory=dict)

    types: dict = field(default_factory=dict)

    constant_values: dict = field(default_factory=dict)

    elaboration: ElaborationModel = field(
        default_factory=ElaborationModel,
    )

    optimization_context: OptimizationContext = field(
        default_factory=OptimizationContext,
    )

    diagnostics: list = field(default_factory=list)

    syntax_tree: object | None = None

