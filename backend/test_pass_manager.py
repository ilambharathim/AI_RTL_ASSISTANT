from app.compiler.pass_manager import PassManager


called = []


def first(*_):

    called.append("first")


def second(*_):

    called.append("second")


manager = PassManager()

manager.register(first)

manager.register(second)

manager.run()

assert called == [

    "first",

    "second",

]

print("PassManager test passed.")

