from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    split = markdown.split("\n\n")
    for block in split:
        stripped = block.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks

def block_to_block_type(markdown_block):
    if re.findall(r"^#{1,6} ", markdown_block):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in markdown_block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in markdown_block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(re.findall(r"^\d+\. ", line) for line in markdown_block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH