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
            # Resolve actual line/column from the diagnostic location.
            #
            line = 1
            column = 1
            if repair.location is not None:
                line = repair.location.line
                column = repair.location.column

            patch = SourcePatch(

                operation="insert",

                line=line,

                column=column,

                text=repair.replacement + "\n",

            )


            patches.append(
                patch,
            )

        semantic_model.source_patches = patches

        return patches
