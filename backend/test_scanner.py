from app.parsers.specification.scanner import Scanner

scanner = Scanner("ABC")

print("\n===== Scanner API Test =====\n")

print("Current :", scanner.current)
print("Peek    :", scanner.peek())

state = scanner.save_state()

scanner.advance()
scanner.advance()

print("\nAfter Advance")
print("Current :", scanner.current)

scanner.restore_state(state)

print("\nAfter Restore")
print("Current :", scanner.current)
print("Position:", scanner.position())

print("\nEOF :", scanner.eof())
