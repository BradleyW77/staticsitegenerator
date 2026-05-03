from enum import Enum

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
