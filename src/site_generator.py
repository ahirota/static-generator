import os, shutil
from block_parser import markdown_to_blocks, markdown_to_html_node

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

def extract_title(markdown):
    title = ""
    md_blocks = markdown_to_blocks(markdown)
    for line in md_blocks:
        if line.startswith("# "):
            # Quit on FIRST Find
            title = line[2:]
            break
    if title == "":
        raise Exception("No H1 Title Found in Markdown")
    return title

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.isfile(from_path):
        raise Exception(f"{from_path} is not a valid markdown file.")
    
    print(f"Generating Page from {from_path} to {dest_path}, using {template_path}.")
    # Get Markdown
    raw_md = open(from_path).read()

    # Get Template
    if not os.path.isfile(template_path):
        raise Exception(f"{template_path} is not a valid template file.")
    template = open(template_path).read()


    # Build HTML File
    title = extract_title(raw_md)
    node = markdown_to_html_node(raw_md)
    html = node.to_html()
    generated = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")

    # Check and Create Sub Folders if they exist
    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)

    # Write HTML
    html_file = open(dest_path, 'w', encoding="utf-8")
    html_file.write(generated)
    html_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Check and Make Public Directory Subfolders
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    # Loop through Content Directory
    for filename in os.listdir(dir_path_content):
        # Get Content Folder/Markdown File
        content_path = os.path.join(dir_path_content, filename)

        # If Markdown File Found
        if os.path.isfile(content_path):
            # Create New Path Name by swapping file extensions
            htmlified_name = filename.replace(".md",".html")
            dest_path = os.path.join(dest_dir_path, htmlified_name)

            generate_page(content_path,template_path,dest_path, basepath)
        # Else Folder, Recursively Call Generate Page
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
