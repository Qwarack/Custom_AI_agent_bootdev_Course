from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(result)
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

test_cases = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
]

for test in test_cases:
    print(get_file_content(*test))
