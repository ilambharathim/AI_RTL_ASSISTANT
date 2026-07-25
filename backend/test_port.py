from app.domain.port import Port


clk = Port(
    name="clk",
    direction="input",
    datatype="logic",
    width=1
)

rst = Port(
    name="rst_n",
    direction="input",
    datatype="logic",
    width=1
)

data = Port(
    name="data_in",
    direction="input",
    datatype="logic",
    width=32
)

result = Port(
    name="result",
    direction="output",
    datatype="logic",
    width=32
)

ports = [clk, rst, data, result]

print("\n========== PORTS ==========\n")

for port in ports:
    print(port)

print("\n===========================\n")
