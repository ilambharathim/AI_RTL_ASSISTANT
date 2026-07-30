"""
Compiler scope stack.
"""

from app.semantics.scope import Scope
from app.semantics.scope_kind import ScopeKind


class ScopeStack:

    def __init__(self):

        self._stack = [

            Scope(
                name="global",
                kind=ScopeKind.GLOBAL,
            )

        ]

    @property
    def current(
        self,
    ) -> Scope:

        return self._stack[-1]

    def push(
        self,
        name: str,
        kind: ScopeKind,
    ) -> Scope:

        scope = Scope(
            name=name,
            kind=kind,
            parent=self.current,
        )

        self.current.add_child(scope)

        self._stack.append(scope)

        return scope

    def pop(
        self,
    ) -> Scope:

        if len(self._stack) == 1:
            raise RuntimeError(
                "Cannot pop global scope."
            )

        return self._stack.pop()

    @property
    def global_scope(
        self,
    ) -> Scope:

        return self._stack[0]
