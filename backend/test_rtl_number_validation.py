from app.parsers.rtl.readers.number_reader import NumberReader

assert NumberReader._validate_underscore_usage("1000")
assert NumberReader._validate_underscore_usage("1_000")
assert NumberReader._validate_underscore_usage("DEAD_BEEF")

assert not NumberReader._validate_underscore_usage("_100")
assert not NumberReader._validate_underscore_usage("100_")
assert not NumberReader._validate_underscore_usage("1__000")

print("RTL number underscore validation test passed.")
