from app.semantics.scope_kind import ScopeKind
from app.semantics.scope_stack import ScopeStack
from app.semantics.symbol import Symbol
from app.semantics.symbol_kind import SymbolKind

stack = ScopeStack()

stack.current.define(
    Symbol(
        name="WIDTH",
        kind=SymbolKind.PARAMETER,
    )
)

assert stack.current.lookup("WIDTH") is not None

stack.push(
    "adder",
    ScopeKind.MODULE,
)

stack.current.define(
    Symbol(
        name="sum",
        kind=SymbolKind.SIGNAL,
    )
)

assert stack.current.lookup("sum") is not None

assert stack.current.lookup("WIDTH") is not None

stack.pop()

assert stack.current.lookup("WIDTH") is not None

print("Symbol table test passed.")
