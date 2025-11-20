import unittest

from textnode import TextNode, TextType
from parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some more text here.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and some more text here.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_no_text_between_but_text_after(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)[and another](https://www.youtube.com/@bootdotdev) but this is text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("and another", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" but this is text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an image ![see me here](https://i.imgur.com/3elNhQu.png) and a link [click me!](https://www.urlhere.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ![see me here](https://i.imgur.com/3elNhQu.png) and a link ", TextType.TEXT),
                TextNode(
                    "click me!", TextType.LINK, "https://www.urlhere.com/"
                ),
            ],
            new_nodes,
        )
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("see me here", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode(
                    "click me!", TextType.LINK, "https://www.urlhere.com/"
                ),
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()