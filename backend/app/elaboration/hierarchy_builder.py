"""
Hierarchy Tree Builder.
Constructs resolved HierarchyNode trees from syntax trees and semantic models.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set

from app.ast import CompilationUnit, ModuleDeclaration, ModuleInstance
from app.elaboration.hierarchy_node import HierarchyNode


class HierarchyTreeBuilder:
    """
    Builds a tree of HierarchyNodes representing the design hierarchy.
    """

    def _collect_instances(self, items) -> List[ModuleInstance]:
        instances: List[ModuleInstance] = []
        if not items:
            return instances

        if not isinstance(items, (list, tuple)):
            items = [items]

        for item in items:
            if isinstance(item, ModuleInstance):
                instances.append(item)
            elif hasattr(item, "members") and item.members:
                instances.extend(self._collect_instances(item.members))
            elif hasattr(item, "statements") and item.statements:
                instances.extend(self._collect_instances(item.statements))
            elif hasattr(item, "body") and item.body:
                instances.extend(self._collect_instances(item.body))
            elif hasattr(item, "then_branch") and item.then_branch:
                instances.extend(self._collect_instances(item.then_branch))
            elif hasattr(item, "else_branch") and item.else_branch:
                instances.extend(self._collect_instances(item.else_branch))
        return instances

    def build_tree(
        self,
        syntax_tree: CompilationUnit,
        top_module_name: Optional[str] = None,
    ) -> List[HierarchyNode]:
        """
        Builds hierarchy tree(s) starting from top-level module(s).
        If top_module_name is specified, builds starting from that module.
        Otherwise, automatically detects top-level modules (modules not instantiated elsewhere).
        """
        modules_by_name: Dict[str, ModuleDeclaration] = {}
        instantiated_modules: Set[str] = set()

        for declaration in syntax_tree.declarations:
            if isinstance(declaration, ModuleDeclaration):
                modules_by_name[declaration.name] = declaration
                instances = self._collect_instances(declaration.members)
                for inst in instances:
                    instantiated_modules.add(inst.module_name)

        if top_module_name:
            top_names = [top_module_name] if top_module_name in modules_by_name else []
        else:
            top_names = [
                name for name in modules_by_name if name not in instantiated_modules
            ]
            if not top_names and modules_by_name:
                top_names = [next(iter(modules_by_name))]

        trees: List[HierarchyNode] = []
        for name in top_names:
            trees.append(self._build_node(name, name, modules_by_name, set()))
        return trees

    def _build_node(
        self,
        name: str,
        module_name: str,
        modules_by_name: Dict[str, ModuleDeclaration],
        visited: Set[str],
    ) -> HierarchyNode:
        children: List[HierarchyNode] = []
        if module_name in modules_by_name and module_name not in visited:
            visited_copy = set(visited)
            visited_copy.add(module_name)
            module_decl = modules_by_name[module_name]

            instances = self._collect_instances(module_decl.members)
            for inst in instances:
                child_node = self._build_node(
                    name=inst.instance_name,
                    module_name=inst.module_name,
                    modules_by_name=modules_by_name,
                    visited=visited_copy,
                )
                children.append(child_node)

        return HierarchyNode(
            name=name,
            module_name=module_name,
            children=children,
        )
