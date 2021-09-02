import os


def is_source_clang(directory: str) -> bool:
    return _directory_contains_file(directory, ".c")


def is_source_cpp(directory: str) -> bool:
    return _directory_contains_file(directory, ".cpp")


def is_source_sol(directory: str) -> bool:
    return _directory_contains_file(directory, ".sol")


def is_source_rust(directory: str) -> bool:
    return _directory_contains_file(directory, "Cargo.toml")


def _directory_contains_file(directory: str, name_suffix: str) -> bool:
    for file in os.listdir(directory):
        if file.lower().endswith(name_suffix.lower()):
            return True
    return False
