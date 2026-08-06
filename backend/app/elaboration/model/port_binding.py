"""
Port binding.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class PortBinding:

    port_name: str

    expression: object = None

