from pathlib import Path

def print_directory_structure(path, indent=0):
    path = Path(path)
    for item in path.iterdir():
        if item.is_dir() and item.name == "venv":
            continue  # Skip the "venv" directory
        print(" " * indent + "|-- " + item.name)
        if item.is_dir():
            print_directory_structure(item, indent + 4)

# Specify the directory
directory_to_scan = Path("")  # Change to your target directory
print_directory_structure(directory_to_scan)