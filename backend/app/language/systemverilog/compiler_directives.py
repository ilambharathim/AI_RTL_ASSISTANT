"""
IEEE 1800 SystemVerilog compiler directives.
"""

SYSTEMVERILOG_COMPILER_DIRECTIVES = frozenset(
    {
        "define",
        "undef",

        "ifdef",
        "ifndef",
        "elsif",
        "else",
        "endif",

        "include",

        "timescale",

        "celldefine",
        "endcelldefine",

        "default_nettype",
        "line",
        "resetall",
        "pragma",

        "begin_keywords",
        "end_keywords",

        "unconnected_drive",
        "nounconnected_drive",
    }
)
