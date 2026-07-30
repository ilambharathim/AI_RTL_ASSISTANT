"""
Deterministic macro storage.
"""


class MacroTable:

    def __init__(self):

        self._table: dict[str, str] = {}

    def define(
        self,
        name: str,
        value: str,
    ) -> None:

        self._table[name] = value

    def undef(
        self,
        name: str,
    ) -> None:

        self._table.pop(name, None)

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._table

    def lookup(
        self,
        name: str,
    ) -> str | None:

        return self._table.get(name)
