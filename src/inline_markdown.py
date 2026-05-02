import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 != 1:
                raise ValueError("Invalid Markdown syntax: uneven number of delimiters!")
            else:
                for i, part in enumerate(parts):
                    if part == "":
                        continue
                    if i % 2 == 1:  # This is the text between delimiters
                        new_nodes.append(TextNode(part, text_type))
                    else:
                        new_nodes.append(TextNode(part, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    images_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(images_pattern, text)

def extract_markdown_links(text):
    links_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(links_pattern, text)
