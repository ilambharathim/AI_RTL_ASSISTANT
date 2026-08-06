"""
Patch Generator.
"""

from app.repair.patches.source_patch import (
    SourcePatch,
)


class PatchGenerator:

    def generate(
        self,
        semantic_model,
    ):

        patches = []

        repairs = getattr(
            semantic_model,
            "repairs",
            [],
        )

        for repair in repairs:

            if repair.replacement is None:
                continue

            #
            # Temporary insertion point.
            #
            # Later this will come from AST source locations.
            #
            patch = SourcePatch(

                operation="insert",

                line=1,

                column=1,

                text=repair.replacement + "\n",

            )

            patches.append(
                patch,
            )

        semantic_model.source_patches = patches

        return patches
