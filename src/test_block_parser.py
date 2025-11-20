import unittest

from block_parser import markdown_to_blocks

class TestParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_from_example(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_with_hella_newlines(self):
        md = """
# This is a header


This is a paragraph with an extra new line above this
This is the same paragraph on a new line






- This is a list with EXCESSIVE newlines above this
- and an item here
- and another one here with a few extra newlines below this



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a header",
                "This is a paragraph with an extra new line above this\nThis is the same paragraph on a new line",
                "- This is a list with EXCESSIVE newlines above this\n- and an item here\n- and another one here with a few extra newlines below this",
            ],
        )

if __name__ == "__main__":
    unittest.main()