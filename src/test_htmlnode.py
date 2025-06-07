import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_obj_prop(self):
        node = HTMLNode('h1', 'Header Text')
        self.assertEqual(node.tag, 'h1')
        self.assertEqual(node.value, 'Header Text')
        self.assertEqual(node.children, None)
        self.assertNotEqual(node.props, {'data-attr':'attribute'})

    def test_props_to_html(self):
        node = HTMLNode('a', 'Click Me', 'children', {'href':'https://www.boot.dev', 'target':'_blank'})
        intended = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), intended)

    def test_repr(self):
        node = HTMLNode('a', 'Click Me', 'children', {'href':'https://www.boot.dev', 'target':'_blank'})
        intended = "HTMLNode(tag=a, value=Click Me, children=children, props={'href': 'https://www.boot.dev', 'target': '_blank'})"
        self.assertEqual(str(node), intended)


if __name__ == '__main__':
    unittest.main()