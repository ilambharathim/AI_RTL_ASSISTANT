"""
RTL lexical token readers.

Each reader is responsible for recognizing exactly one family of
SystemVerilog lexical tokens.

The RTLLexer coordinates these readers while remaining small and
deterministic.
"""
