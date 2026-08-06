from app.semantics.symbols.symbol_info import SymbolInfo

symbol = SymbolInfo(

    name="data",

    symbol_type="logic",

    width=8,

)

assert symbol.name == "data"

assert symbol.symbol_type == "logic"

assert symbol.width == 8

assert symbol.signed is False

print("SymbolInfo test passed.")
