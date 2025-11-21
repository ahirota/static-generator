from enum import Enum
import re

from htmlnode import ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_parser import text_to_textnodes

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
    elif markdown_block.startswith("1. "):
        i = 1
        for line in markdown_block.split("\n"):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
# THE BEAST STARTS
def markdown_to_html_node(markdown):
    children = []
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        # Determine the type of block
        block_type = block_to_block_type(block)
        html_block = block_to_html(block, block_type)
        children.append(html_block)    
    # Make all the block nodes children under a single parent HTML node
    return ParentNode("div", children)

def block_to_html(block,block_type):
    if block_type == BlockType.CODE:
        # Strip first 3 and last 3 characters (`), Then wrap in code, and wrap that in pre
        # No text to markdown inside the code block
        block_text = block[3:-3]
        # Strip Leading Newline if that exists I guess
        if block_text[0] == "\n":
            block_text = block_text[1:]
        return ParentNode("pre",[LeafNode("code", block_text)])
    
    elif block_type == BlockType.HEADING:
        # Check Number of #'s based on first space split length
        # We're assuming it's already good Markdown
        header = block.split(" ", 1)
        children = text_to_children(header[1])
        return ParentNode(f"h{len(header[0])}", children)
    
    elif block_type == BlockType.UNORDERED_LIST:
        children = []
        for line in block.split("\n"):
            # Remove Quote "- " From the lines
            block_text = line[2:]
            # Each Line is a list item Parent Node with childnodes that need to be Parsed
            list_item = ParentNode("li", text_to_children(block_text))
            children.append(list_item)
        return ParentNode("ul", children)
    
    elif block_type == BlockType.ORDERED_LIST:
        children = []
        for line in block.split("\n"):
            # Remove Quote "{digit}. " From the lines
            block_text = line[3:]
            # Each Line is a list item Parent Node with childnodes that need to be Parsed
            children.append(ParentNode("li", text_to_children(block_text)))
        return ParentNode("ol",children)
    
    elif block_type == BlockType.QUOTE:
        lines = []
        for line in block.split("\n"):
            # Remove Quote ">" From the lines
            # Need to strip from Quote and rejoin because that's the intended functionality
            lines.append(line.lstrip(">").strip())
        block_text = " ".join(lines)
        children = text_to_children(block_text)
        return ParentNode("blockquote", children)

    else:
        children = []
        for line in block.split("\n"):
            children.extend(text_to_children(line))
        return ParentNode("p", children)
    
def text_to_children(text):
    # Takes a SINGLE LINE of text
    # Returns List of Leaf or Parent Nodes with Leaves inside
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children