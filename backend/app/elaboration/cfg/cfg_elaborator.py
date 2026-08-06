"""
CFG Elaborator.

Builds a Control Flow Graph for each elaborated module.
"""

from app.analysis.cfg import CFGBuilder


class CFGElaborator:

    def elaborate(
        self,
        semantic_model,
    ):

        builder = CFGBuilder()

        elaboration = semantic_model.elaboration

        if not hasattr(
            elaboration,
            "cfgs",
        ):

            elaboration.cfgs = {}

        #
        # Build one CFG per elaborated module.
        #
        for module_name, module in (
            elaboration.elaborated_modules.items()
        ):

            elaboration.cfgs[module_name] = (

                builder.build(
                    module,
                )

            )
