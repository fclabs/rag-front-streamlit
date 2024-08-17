import os

def read_file_text(filename: str) -> str:
    """Read the content of a file and return it as a string.
    Args:
        filename (str): The name of the file to read.
    """
    try:
        with open(filename, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = f"{filename} not found. Path: {os.getcwd()}"
    return content