import os, shutil

def copy_to_public_recursive(from_dir, to_dir):
    # Check and Make Public Directory
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)

    # Get all filepaths in from directory
    for filename in os.listdir(from_dir):
        from_path = os.path.join(from_dir, filename)
        to_path = os.path.join(to_dir, filename)
        print(f"Copying {from_path} to {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_to_public_recursive(from_path, to_path)


def copy_to_public_copytree(from_dir, to_dir):
    # Check and Make Public Directory
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    shutil.copytree(from_dir, to_dir, dirs_exist_ok=True)