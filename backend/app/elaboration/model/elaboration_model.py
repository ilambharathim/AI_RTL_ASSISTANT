"""
RIVA Elaboration Model.

Stores all information produced during elaboration.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ElaborationModel:

    #
    # Parameter resolution
    #
    instance_parameters: dict = field(
        default_factory=dict,
    )

    #
    # Hierarchy
    #
    hierarchy: dict = field(
        default_factory=dict,
    )

    elaborated_modules: dict = field(
        default_factory=dict,
    )


    #
    # Port binding
    #
    port_bindings: dict = field(
        default_factory=dict,
    )

    #
    # Signal resolution
    #
    resolved_signals: dict = field(
        default_factory=dict,
    )

    #
    # RTL graph
    #
    rtl_graph: dict = field(
        default_factory=dict,
    )

    #
    # Netlist
    #
    netlist: dict = field(
        default_factory=dict,
    )

    #
    # Typed Intermediate Representation (IR)
    #
    ir: dict = field(
        default_factory=dict,
    )
