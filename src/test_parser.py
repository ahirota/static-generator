import unittest

from textnode import TextNode, TextType
from parser import split_nodes_delimiter

class TestParser(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_raises_error(self):
        node = TextNode("This is text with a `code block` word and a floating delimiter `", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node],"`",TextType.CODE)

    def test_multiple_delim(self):
        node = TextNode("This is `text` with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_delim(self):
        node = TextNode("This is **bold text** with a `code block` word (we're ignoring the code)", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with a `code block` word (we're ignoring the code)", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_and_ital_delim(self):
        node = TextNode("This is **bold text** with an _italic word_ inside.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(" inside.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()