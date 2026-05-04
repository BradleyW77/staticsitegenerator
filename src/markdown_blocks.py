from enum import Enum

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            new_blocks.append(block)
    return new_blocks

class BlockType(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    UnorderedList = "unordered_list"
    OrderedList = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.Heading
    elif lines[0].startswith("```") and len(lines) > 1 and lines[-1] == "```":
        return BlockType.Code
    elif len(lines) > 0 and (lines[0].startswith(">")) and all((line.startswith(">")) for line in lines[1:]):
        return BlockType.Quote
    elif len(lines) > 0 and lines[0].startswith("- ") and all(line.startswith("- ") for line in lines[1:]):
        return BlockType.UnorderedList
    elif len(lines) > 0 and lines[0].startswith("1. ") and all(line.startswith(f"{i + 2}. ") for i, line in enumerate(lines[1:])):
        return BlockType.OrderedList
    else:
        return BlockType.Paragraph

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # Handle each block type
        # Handles heading blocks
        if block_type == BlockType.Heading:
            if block.startswith("# "):
                html_nodes.append(ParentNode(tag="h1", children=text_to_children(block[2:])))
            elif block.startswith("## "):
                html_nodes.append(ParentNode(tag="h2", children=text_to_children(block[3:])))
            elif block.startswith("### "):
                html_nodes.append(ParentNode(tag="h3", children=text_to_children(block[4:])))
            elif block.startswith("#### "):
                html_nodes.append(ParentNode(tag="h4", children=text_to_children(block[5:])))
            elif block.startswith("##### "):
                html_nodes.append(ParentNode(tag="h5", children=text_to_children(block[6:])))
            elif block.startswith("###### "):
                html_nodes.append(ParentNode(tag="h6", children=text_to_children(block[7:])))
        # Handles code blocks
        elif block_type == BlockType.Code:
            lines = block.split("\n")
            inner = lines[1:-1]
            result = "\n".join(inner) + "\n"
            leafnode = LeafNode(tag="code", value=result)
            parentnode = ParentNode(tag="pre", children=[leafnode])
            html_nodes.append(parentnode)
        # Handles quote blocks
        elif block_type == BlockType.Quote:
            # Remove the "> " prefix from each line and join them
            lines = block.split("\n")
            result = " ".join(line[2:] for line in lines if line.strip("> "))
            html_nodes.append(ParentNode(tag="blockquote", children=text_to_children(result)))
        # Handles unordered list blocks
        elif block_type == BlockType.UnorderedList:
            html_nodes.append(ParentNode(tag="ul", children=[ParentNode(tag="li", children=text_to_children(line[2:])) for line in block.split("\n") if line.strip()]))
        # Handles ordered list blocks
        elif block_type == BlockType.OrderedList:
            html_nodes.append(ParentNode(tag="ol", children=[ParentNode(tag="li", children=text_to_children(line[3:])) for line in block.split("\n") if line.strip()]))
        # Handles paragraph blocks
        else:
            block = block.replace("\n", " ")
            html_nodes.append(ParentNode(tag="p", children=text_to_children(block)))
    # Create a parent HTML node to wrap all the child nodes
    parent_html_node = ParentNode(tag="div", children=html_nodes)
    return parent_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No title found in markdown")
