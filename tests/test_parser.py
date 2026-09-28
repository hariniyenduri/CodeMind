from pathlib import Path

from src.processing.code_parser import parse_code_file

sample_code = """
import os
from database import connect_database


def login(username, password):
    if username == "admin":
        return True

    return False


class User:

    def __init__(self, username):
        self.username = username

    def logout(self):
        return True
"""


parsed = parse_code_file(
    Path("auth.py"),
    sample_code,
    "Python",
)


print("\n========== FUNCTIONS ==========")

for function in parsed.functions:
    print(function)


print("\n========== CLASSES ==========")

for class_info in parsed.classes:
    print(class_info)


print("\n========== IMPORTS ==========")

for import_info in parsed.imports:
    print(import_info)
