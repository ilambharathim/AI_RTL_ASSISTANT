from dataclasses import dataclass, field
from typing import List

from app.domain.metadata import Metadata
from app.domain.port import Port
from app.domain.requirement import Requirement


@dataclass(slots=True)
class SpecificationIR:
    """
    Intermediate Representation (IR) of a hardware specification.

    Every specification parser must return this object.
    Every verification engine must consume this object.
    """

    metadata: Metadata = field(default_factory=Metadata)

    ports: List[Port] = field(default_factory=list)

    requirements: List[Requirement] = field(default_factory=list)

    parameters: List[str] = field(default_factory=list)

    timing_requirements: List[str] = field(default_factory=list)

    constraints: List[str] = field(default_factory=list)

    assertions: List[str] = field(default_factory=list)

    protocols: List[str] = field(default_factory=list)
