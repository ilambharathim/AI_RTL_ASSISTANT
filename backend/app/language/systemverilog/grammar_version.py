from enum import Enum


class SystemVerilogVersion(str, Enum):
    """
    Supported IEEE SystemVerilog language revisions.
    """

    IEEE_1800_2005 = "IEEE1800-2005"
    IEEE_1800_2009 = "IEEE1800-2009"
    IEEE_1800_2012 = "IEEE1800-2012"
    IEEE_1800_2017 = "IEEE1800-2017"
    IEEE_1800_2023 = "IEEE1800-2023"


DEFAULT_SYSTEMVERILOG_VERSION = (
    SystemVerilogVersion.IEEE_1800_2023
)
