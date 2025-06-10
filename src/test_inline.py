import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

if __name__ == '__main__':
    unittest.main()