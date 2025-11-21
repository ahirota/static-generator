import os, shutil
from site_generator import copy_to_public_recursive, copy_to_public_copytree, generate_pages_recursive

# Executing From Root Folder (not src)
static = "./static"
public = "./public"

def main():
    print("Deleting public directory")
    if os.path.exists(public):
        shutil.rmtree(public)

    # The commented uses copytree to avoid recursion
    # copy_to_public_copytree(static, public)
    copy_to_public_recursive(static, public)

    # Generate Pages by Recursively Crawling the Content Directory
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()