import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected = "TextNode(This is a text node, bold, None)"
        self.assertEqual(str(node), expected)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://thistechnicallydoesntmatter.com")
        self.assertNotEqual(node, node2)


    def test_not_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        # None != none
        expected = "TextNode(This is a text node, bold, none)"
        self.assertNotEqual(str(node), expected)

class TestTextNodeToLeafNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_text_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_text_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_text_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"https://www.url.com"})
        self.assertEqual(html_node.props_to_html(), " href=\"https://www.url.com\"")

    def test_text_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":"https://www.url.com", "alt":"This is an image node"})
        self.assertEqual(html_node.props_to_html(), " src=\"https://www.url.com\" alt=\"This is an image node\"")



if __name__ == "__main__":
    unittest.main()