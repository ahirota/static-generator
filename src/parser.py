import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            split = node.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("Text Node contains uneven number of delimiters, unable to split properly")
            for i in range(len(split)):
                if i % 2 == 0:
                    split_nodes.append(TextNode(split[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(split[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)