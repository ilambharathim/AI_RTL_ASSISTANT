"""
Generic compiler pass manager.
"""


class PassManager:

    def __init__(self):

        self._passes = []

    def register(
        self,
        compiler_pass,
    ):

        self._passes.append(
            compiler_pass,
        )

    def run(
        self,
        *args,
    ):

        result = None

        for compiler_pass in self._passes:

            result = compiler_pass(*args)

        return result

