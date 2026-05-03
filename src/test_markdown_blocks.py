import unittest

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block of text."])

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.Paragraph)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.Heading)
    
    def test_block_to_block_type_heading_level_6(self):
        block = "###### This is a heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.Heading)

    def test_block_to_block_type_code(self):
        block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.Code)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> This is another quote"
        self.assertEqual(block_to_block_type(block), BlockType.Quote)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list item\n- This is another list item"
        self.assertEqual(block_to_block_type(block), BlockType.UnorderedList)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"
        self.assertEqual(block_to_block_type(block), BlockType.OrderedList)

if __name__ == "__main__":
    unittest.main()
