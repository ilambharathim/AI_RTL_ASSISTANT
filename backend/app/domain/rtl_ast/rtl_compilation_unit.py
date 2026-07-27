from dataclasses import dataclass, field

from app.domain.rtl_ast.module_node import ModuleNode


@dataclass(slots=True)
class RTLCompilationUnit:
    """
    Root container for parsed RTL files.
    """

    modules: list[ModuleNode] = field(default_factory=list)

    def add_module(self, module: ModuleNode) -> None:
        if not isinstance(module, ModuleNode):
            raise TypeError("module must be a ModuleNode.")
        self.modules.append(module)

    @property
    def module_count(self) -> int:
        return len(self.modules)
