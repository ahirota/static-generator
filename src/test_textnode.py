import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT)
        intended = "TextNode(This is a text node, text, None)"
        self.assertEqual(str(node), intended)

    def test_obj_prop(self):
        node = TextNode("img alt here", TextType.IMAGE, "https://www.test.com/asset.jpg")
        self.assertEqual(node.url, "https://www.test.com/asset.jpg")

    def test_obj_prop_not_eq(self):
        node = TextNode("text", TextType.ITALIC)
        self.assertNotEqual(node.url, "")


if __name__ == "__main__":
    unittest.main()