"""
Base Repair Rule.
"""


class RepairRule:

    code = ""

    def repair(
        self,
        diagnostic,
        semantic_model,
    ):

        raise NotImplementedError
