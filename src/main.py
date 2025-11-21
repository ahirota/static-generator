import os, shutil, sys
from site_generator import copy_to_public_recursive, copy_to_public_copytree, generate_pages_recursive

# Executing From Root Folder (not src)
static = "./static"
public = "./public"
content = "./content"
template = "./template.html"
docs = "./docs"

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting docs directory")
    if os.path.exists(docs):
        shutil.rmtree(docs)

    # The commented uses copytree to avoid recursion
    # copy_to_public_copytree(static, public)
    copy_to_public_recursive(static, docs)

    # Generate Pages by Recursively Crawling the Content Directory
    generate_pages_recursive(content, template, docs, basepath)

if __name__ == "__main__":
    main()