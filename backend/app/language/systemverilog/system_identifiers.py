"""
IEEE 1800 SystemVerilog system tasks and system functions.

This list will be expanded over time toward full IEEE coverage.
"""

SYSTEMVERILOG_SYSTEM_IDENTIFIERS = frozenset(
    {
        "display",
        "write",
        "monitor",
        "strobe",

        "finish",
        "stop",
        "exit",

        "time",
        "stime",
        "realtime",

        "random",
        "urandom",
        "urandom_range",

        "clog2",
        "bits",
        "typename",
        "size",

        "signed",
        "unsigned",

        "fopen",
        "fclose",
        "fdisplay",
        "fwrite",
        "fscanf",

        "readmemh",
        "readmemb",

        "dumpfile",
        "dumpvars",
    }
)
