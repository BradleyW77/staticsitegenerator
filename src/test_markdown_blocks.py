import unittest

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, extract_title

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

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = "> This is a quote\n\n> This is another quote"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><blockquote>This is a quote</blockquote><blockquote>This is another quote</blockquote></div>",
        )
    
    def test_unordered_list(self):
        md = "- This is a list item\n- This is another list item"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ul><li>This is a list item</li><li>This is another list item</li></ul></div>",
        )
    
    def test_ordered_list(self):
        md = "1. This is a list item\n2. This is another list item"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ol><li>This is a list item</li><li>This is another list item</li></ol></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_no_block(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a title"
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_title(self):
        md = "This is not a title"
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
