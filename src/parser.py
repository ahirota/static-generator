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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        else:
            split_nodes = []
            to_parse = node.text
            for img in images:
                sections = to_parse.split(f"![{img[0]}]({img[1]})", 1)
                if sections[0] and sections[0] != "":
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                to_parse = sections[1] if len(sections) >= 2 else ""
            if to_parse != "":
                split_nodes.append(TextNode(to_parse, TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        else:
            split_nodes = []
            to_parse = node.text
            for link in links:
                sections = to_parse.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] and sections[0] != "":
                    split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                to_parse = sections[1] if len(sections) >= 2 else ""
            if to_parse != "":
                split_nodes.append(TextNode(to_parse, TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes