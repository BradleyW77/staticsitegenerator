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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            images = extract_markdown_images(node.text)
            if images:
                for image in images:
                    sections = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
                    if sections:
                        if sections[0]:
                            new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                        remaining_text = sections[1] if len(sections) > 1 else ""
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            links = extract_markdown_links(node.text)
            if links:
                for link in links:
                    sections = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
                    if sections:
                        if sections[0]:
                            new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                        remaining_text = sections[1] if len(sections) > 1 else ""
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
