"""
RIVA Elaborator.
"""

from app.elaboration.parameters.parameter_elaborator import ParameterElaborator
from app.elaboration.generate.generate_elaborator import GenerateElaborator
from app.elaboration.hierarchy.hierarchy_elaborator import HierarchyElaborator
from app.elaboration.instances.instance_resolver import InstanceResolver
from app.elaboration.modules.module_resolver import ModuleResolver
from app.elaboration.ports.port_binder import PortBinder
from app.elaboration.signals.signal_resolver import SignalResolver
from app.elaboration.rtl_graph.rtl_graph_builder import RTLGraphBuilder
from app.elaboration.netlist.netlist_builder import NetlistBuilder


class Elaborator:

    def __init__(self):

        self.parameter_elaborator = ParameterElaborator()

        self.generate_elaborator = GenerateElaborator()

        self.hierarchy_elaborator = HierarchyElaborator()

        self.instance_resolver = InstanceResolver()

        self.module_resolver = ModuleResolver()

        self.port_binder = PortBinder()

        self.signal_resolver = SignalResolver()

        self.rtl_graph_builder = RTLGraphBuilder()

        self.netlist_builder = NetlistBuilder()

    def elaborate(
        self,
        syntax_tree,
        semantic_model,
    ):

        self.parameter_elaborator.elaborate(
            syntax_tree,
            semantic_model,
        )

        self.generate_elaborator.elaborate(
            syntax_tree,
            semantic_model,
        )

        self.hierarchy_elaborator.elaborate(
            syntax_tree,
            semantic_model,
        )

        self.module_resolver.resolve(
            syntax_tree,
            semantic_model,
        )

        self.instance_resolver.resolve(
            syntax_tree,
            semantic_model,
        )

        self.port_binder.bind(
            semantic_model,
        )

        self.signal_resolver.resolve(
            semantic_model,
        )

        self.rtl_graph_builder.build(
            semantic_model,
        )

        self.netlist_builder.build(
            semantic_model,
        )

        return semantic_model

