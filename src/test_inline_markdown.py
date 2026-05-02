import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_italic(self):
        # Test case 1: Italic case
        nodes = [TextNode("Hello _world_!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, "!")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_bold(self):
        # Test case 2: Bold case
        nodes = [TextNode("Hello **world**!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "!")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_code(self):
        # Test case 3: Code case
        nodes = [TextNode("Hello `world`!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "!")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple(self):
        # Test case 4: Multiple delimiters
        nodes = [TextNode("Hello _world_ and **universe**!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        result = split_nodes_delimiter(result, "**", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "universe")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "!")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_nonText(self):
        # Test case 5: Non-text nodes
        nodes = [TextNode("Hello world!", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(result, nodes)
    
    def test_split_nodes_delimiter_no_delimiter_plain_text(self):
        # Test case 6: No delimiters in plain text
        nodes = [TextNode("Hello world!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(result, nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello world!")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_unmatched_delimiters(self):
        # Test case 7: Unmatched delimiters
        nodes = [TextNode("Hello _world!", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "_", TextType.ITALIC)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and an ![image2](https://i.imgur.com/another.png)"
        )
        self.assertListEqual([
            ("image1", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "https://i.imgur.com/another.png")
        ], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a [link1](https://www.google.com) and a [link2](https://www.github.com)"
        )
        self.assertListEqual([
            ("link1", "https://www.google.com"),
            ("link2", "https://www.github.com")
        ], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

if __name__ == "__main__":
    unittest.main()
