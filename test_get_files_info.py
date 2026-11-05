from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]

for test in test_cases:
    print(get_files_info(*test))
