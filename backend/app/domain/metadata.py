from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass(slots=True)
class Metadata:
    """
    Common metadata describing any engineering artifact.

    This model is shared by specifications, RTL, testbenches,
    reports, and verification results.
    """

    project_name: str = ""

    module_name: str = ""

    description: str = ""

    language: str = ""

    version: str = "1.0"

    author: Optional[str] = None

    organization: Optional[str] = None

    source_file: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    tags: List[str] = field(default_factory=list)
