import os

def clear_output_folder(output_dir="output"):
    """
    Removes all files and subfolders inside the given 'output_dir', but leaves
    the directory itself intact. If you want to remove only files while
    keeping subfolders, remove the 'shutil.rmtree(file_path)' part.

    :param output_dir: (str) Path to the folder to clear. Defaults to 'output'.
    """
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        print(f"The folder '{output_dir}' does not exist.")