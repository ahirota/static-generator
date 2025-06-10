import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            split = node.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("invalid markdown")
            for i in range(len(split)):
                if split[i] == "":
                    continue
                if i % 2 != 0:
                    split_nodes.append(TextNode(split[i], text_type))
                else:
                    split_nodes.append(TextNode(split[i], TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)