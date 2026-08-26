"""
RIVA Semantic Model.

The SemanticModel is the central repository shared by
semantic analysis, diagnostics, elaboration, optimization,
and repair.
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

    The legacy ``types`` dictionary is intentionally retained
    for compatibility while semantic-type objects are migrated
    into ``semantic_types``.
    """

    scopes: dict = field(
        default_factory=dict,
    )

    symbols: dict = field(
        default_factory=dict,
    )

    #
    # Legacy semantic type representation.
    #
    # Existing passes currently store dictionaries here.
    # This remains stable during the migration.
    #
    types: dict = field(
        default_factory=dict,
    )

    #
    # Canonical semantic Type objects.
    #
    # New semantic passes should prefer this repository.
    #
    semantic_types: dict = field(
        default_factory=dict,
    )

    constant_values: dict = field(
        default_factory=dict,
    )

    elaboration: ElaborationModel = field(
        default_factory=ElaborationModel,
    )

    optimization_context: OptimizationContext = field(
        default_factory=OptimizationContext,
    )

    diagnostics: list = field(
        default_factory=list,
    )

    syntax_tree: object | None = None

    def set_semantic_type(
        self,
        name: str,
        semantic_type,
    ):
        """
        Register the canonical semantic type for a symbol.
        """

        self.semantic_types[name] = semantic_type

    def get_semantic_type(
        self,
        name: str,
    ):
        """
        Resolve the canonical semantic type for a symbol.
        """

        return self.semantic_types.get(name)

    def set_constant_value(
        self,
        name: str,
        value,
    ):
        """
        Register a resolved constant value.
        """

        self.constant_values[name] = value

    def get_constant_value(
        self,
        name: str,
    ):
        """
        Retrieve a resolved constant value.
        """

        return self.constant_values.get(name)
