import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr_empty(self):
        node = HTMLNode()
        expected = "HTMLNode(Tag: None, Value: None, Children: None, Props: None)"
        self.assertEqual(str(node), expected)

    def test_repr_eq(self):
        node = HTMLNode(value="This is a text node")
        expected = "HTMLNode(Tag: None, Value: This is a text node, Children: None, Props: None)"
        self.assertEqual(str(node), expected)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        expected = f"HTMLNode(Tag: None, Value: None, Children: None, Props: {str({"href": "https://www.google.com","target": "_blank",})})"
        self.assertEqual(str(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Some Raw Text Here")
        self.assertEqual(node.to_html(), "Some Raw Text Here")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        expected = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(str(node), expected)


if __name__ == "__main__":
    unittest.main()