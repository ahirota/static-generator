import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props_and_children(self):
        grandchild_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("p", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"aria-label": "button"})
        self.assertEqual(
            parent_node.to_html(),
            "<div aria-label=\"button\"><p><a href=\"https://www.google.com\">Click me!</a></p></div>",
        )

    def test_to_html_with_nested_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        p_child_wrapper = ParentNode("p",[
            LeafNode(None, "raw text here followed by a span"),
            LeafNode("span", "nested span here", {"prop": "whatisthisdoinghere?"})
        ])
        parent_node = ParentNode("div", [
            child_node,
            p_child_wrapper
        ])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p>raw text here followed by a span<span prop=\"whatisthisdoinghere?\">nested span here</span></p></div>",
        )


if __name__ == "__main__":
    unittest.main()