"""
RIVA Intermediate Representation package.
"""

#
# Existing synthesis/netlist IR
#
from app.ir.net import Net
from app.ir.netlist import Netlist
from app.ir.netlist_module import NetlistModule
from app.ir.netlist_instance import NetlistInstance

#
# RTL graph
#
from app.ir.rtl.rtl_graph import RTLGraph
from app.ir.rtl.rtl_module import RTLModule
from app.ir.rtl.rtl_instance import RTLInstance

#
# Typed IR
#
from app.ir.ir_node import IRNode

from app.ir.ir_expression import (
    IRExpression,
    IRIdentifier,
    IRLiteral,
    IRUnary,
    IRBinary,
    IRFunctionCall,
)

from app.ir.ir_statement import (
    IRStatement,
    IRAssignment,
    IRIf,
    IRBlock,
    IRAlways,
)

from app.ir.ir_module import IRModule

from app.ir.typed_ir_builder import TypedIRBuilder

__all__ = [
    # Netlist
    "Net",
    "Netlist",
    "NetlistModule",
    "NetlistInstance",

    # RTL Graph
    "RTLGraph",
    "RTLModule",
    "RTLInstance",

    # Typed IR
    "IRNode",
    "IRExpression",
    "IRIdentifier",
    "IRLiteral",
    "IRUnary",
    "IRBinary",
    "IRFunctionCall",
    "IRStatement",
    "IRAssignment",
    "IRIf",
    "IRBlock",
    "IRAlways",
    "IRModule",
    "TypedIRBuilder",
]
