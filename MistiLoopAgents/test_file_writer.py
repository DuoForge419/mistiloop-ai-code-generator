
from file_writer import write_file


# Test 1: Create a new file.
print(
    write_file(
        "generated/hello.ts",
        'export const message = "Hello from MistiLoop";\n'
    )
)

# Test 2: Attempt to write outside workspace.
try:
    write_file(
        "../orchestrator.py",
        "print('This must not be written')"
    )
except ValueError as error:
    print("Blocked outside write:", error)

# Test 3: Attempt to overwrite an existing file.
try:
    write_file(
        "README.md",
        "# Replaced content"
    )
except FileExistsError as error:
    print("Blocked overwrite:", error)
