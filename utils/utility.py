import os 
import json

def get_vrid(file_path):
    """Read the vrid.json file and return the id."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data.get("id")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading {file_path}")
        return None
    
def is_valid_static_route_file(file_path):
    """Check if ipv4staticroute.json exists and contains a non-empty list."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                if isinstance(data, list) and len(data) > 0:
                    return True
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    print(f"Skipping {file_path}: File is empty, missing, or not a valid list.")
    return False
