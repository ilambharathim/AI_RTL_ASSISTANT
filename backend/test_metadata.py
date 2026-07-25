from app.domain.metadata import Metadata


metadata = Metadata(
    project_name="RIVA",
    module_name="mux2to1",
    description="2-to-1 Multiplexer",
    language="SystemVerilog",
    author="Ilam Bharathi"
)

print("\n===== Metadata =====")
print(metadata)

print("\nProject Name :", metadata.project_name)
print("Module Name  :", metadata.module_name)
print("Language     :", metadata.language)
print("Author       :", metadata.author)
print("====================")
