import os, shutil
from site_generator import copy_to_public_recursive, copy_to_public_copytree

# Executing From Root Folder (not src)
static = "./static"
public = "./public"

def main():
    print("Deleting public directory")
    if os.path.exists(public):
        shutil.rmtree(public)

    copy_to_public_recursive(static, public)

    # The following uses copytree to avoid recursion
    # copy_to_public_copytree(static, public)

if __name__ == "__main__":
    main()