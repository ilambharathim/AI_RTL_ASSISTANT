from app.semantics.scope_kind import ScopeKind
from app.semantics.scope_stack import ScopeStack

stack = ScopeStack()

assert stack.current.kind == ScopeKind.GLOBAL

stack.push(
    "adder",
    ScopeKind.MODULE,
)

assert stack.current.name == "adder"

stack.push(
    "always",
    ScopeKind.PROCEDURAL,
)

assert stack.current.kind == ScopeKind.PROCEDURAL

stack.pop()

assert stack.current.name == "adder"

stack.pop()

assert stack.current.kind == ScopeKind.GLOBAL

assert len(stack.global_scope.children) == 1

print("Scope stack test passed.")
