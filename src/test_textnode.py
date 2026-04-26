import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC, "https://www.google.com")
        node4 = TextNode("This is a text node", TextType.PLAIN, "https://www.google.com")
        node5 = TextNode("This is a text node", TextType.PLAIN, "https://www.google.com")

        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)
        self.assertEqual(node4, node5)

if __name__ == "__main__":
    unittest.main()
