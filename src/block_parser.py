def markdown_to_blocks(markdown):
    blocks = []
    split = markdown.split("\n\n")
    for block in split:
        stripped = block.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks