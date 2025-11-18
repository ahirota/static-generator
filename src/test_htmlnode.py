import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_repr_empty(self):
        node = HTMLNode()
        expected = "HTMLNode(Tag: None, Value: None, Children: None, Props: )"
        self.assertEqual(str(node), expected)

    def test_repr_eq(self):
        node = HTMLNode(value="This is a text node")
        expected = "HTMLNode(Tag: None, Value: This is a text node, Children: None, Props: )"
        self.assertEqual(str(node), expected)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        expected = "HTMLNode(Tag: None, Value: None, Children: None, Props:  href=\"https://www.google.com\" target=\"_blank\")"
        self.assertEqual(str(node), expected)


if __name__ == "__main__":
    unittest.main()