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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating Page from {from_path} to {dest_path}, using {template_path}.")
    if not os.path.isfile(from_path):
        raise Exception(f"{from_path} is not a valid markdown file.")
    raw_md = open(from_path).read()

    if not os.path.isfile(template_path):
        raise Exception(f"{template_path} is not a valid template file.")
    template = open(template_path).read()

    title = extract_title(raw_md)

    node = markdown_to_html_node(raw_md)
    html = node.to_html()

    generated = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html)

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)

    f = open(dest_path, 'w', encoding="utf-8")
    f.write(generated)
    f.close()