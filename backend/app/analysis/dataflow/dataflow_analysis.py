"""
Base Data Flow Analysis.
"""

from abc import ABC
from abc import abstractmethod


class DataFlowAnalysis(ABC):

    forward = True

    @abstractmethod
    def transfer(
        self,
        block,
        incoming,
    ):
        ...

    @abstractmethod
    def meet(
        self,
        sets,
    ):
        ...

    @abstractmethod
    def initial(self):
        ...
