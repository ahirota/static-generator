import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title Here")
        self.assertEqual(node.to_html(), "<h1>Title Here</h1>")

    def test_leaf_to_html_plain(self):
        node = LeafNode(None, "No Tags Here")
        self.assertEqual(node.to_html(), "No Tags Here")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )


if __name__ == '__main__':
    unittest.main()