import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter

class TestHTMLNode(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_same(self):
        node = TextNode("`This is code`", TextType.CODE)
        node2 = TextNode("_This is italics_", TextType.ITALIC)
        node3 = TextNode("**This is BOLD**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node,node2,node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node,node2,node3])

    def test_split_nodes_delimiter_multi_tick(self):
        s_node = TextNode("This is text with a ", TextType.TEXT)
        s_node2 = TextNode("code block", TextType.CODE)
        s_node3 = TextNode(" and another ", TextType.TEXT)
        s_node4 = TextNode("code block", TextType.CODE)
        s_node5 = TextNode(" here", TextType.TEXT)
        node = TextNode("This is text with a `code block` and another `code block` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [s_node,s_node2,s_node3,s_node4,s_node5])

    def test_split_nodes_delimiter_fail(self):
        node = TextNode("This is text with a `code block` but too many `backticks", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

if __name__ == '__main__':
    unittest.main()