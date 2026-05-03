import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is text with an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://i.imgur.com/zjjcJKZ.png")
    
    def test_split_nodes_image_no_images(self):
        nodes = [TextNode("This is text with no images", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is text with no images")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_image_multiple_images(self):
        nodes = [TextNode("This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and an ![image2](https://i.imgur.com/another.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This is text with an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "image1")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(result[2].text, " and an ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "image2")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "https://i.imgur.com/another.png")

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        nodes = [TextNode("This is text with a [link](https://www.google.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://www.google.com")

    def test_split_nodes_link_no_links(self):
        nodes = [TextNode("This is text with no links", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is text with no links")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_link_multiple_links(self):
        nodes = [TextNode("This is text with a [link1](https://www.google.com) and a [link2](https://www.github.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link1")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://www.google.com")
        self.assertEqual(result[2].text, " and a ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "link2")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].url, "https://www.github.com")

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " with an ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " word and a ")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[5].text, "code block")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, " and an ")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[7].text, "obi wan image")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(result[8].text, " and a ")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[9].text, "link")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].url, "https://boot.dev")

    def test_text_to_textnodes_empty(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 0)
    
    def test_text_to_textnodes_only_text(self):
        text = "This is just text"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is just text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_text_to_textnodes_only_bold(self):
        text = "**This is bold**"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
    
    def test_text_to_textnodes_only_italic(self):
        text = "_This is italic_"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is italic")
        self.assertEqual(result[0].text_type, TextType.ITALIC)

    def test_text_to_textnodes_only_code(self):
        text = "`This is code`"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is code")
        self.assertEqual(result[0].text_type, TextType.CODE)

    def test_text_to_textnodes_only_image(self):
        text = "![alt text](image.jpg)"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "alt text")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "image.jpg")

    def test_text_to_textnodes_only_link(self):
        text = "[link text](https://example.com)"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "link text")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example.com")

    def test_text_to_textnodes_multiple_images(self):
        text = "![alt text 1](image1.jpg) and ![alt text 2](image2.jpg)"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "alt text 1")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "image1.jpg")
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "alt text 2")
        self.assertEqual(result[2].text_type, TextType.IMAGE)
        self.assertEqual(result[2].url, "image2.jpg")

if __name__ == "__main__":
    unittest.main()
