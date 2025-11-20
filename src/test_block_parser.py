import unittest

from block_parser import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockParser(unittest.TestCase):
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


    def test_block_to_blocktype_header(self):
        md = "# Heading1"
        self.assertEqual(block_to_block_type(md),BlockType.HEADING)
        md = "## Heading2"
        self.assertEqual(block_to_block_type(md),BlockType.HEADING)
        md = "### Heading3"
        self.assertEqual(block_to_block_type(md),BlockType.HEADING)
        md = "#### Heading4"
        self.assertEqual(block_to_block_type(md),BlockType.HEADING)
        md = "##### Heading5"
        self.assertEqual(block_to_block_type(md),BlockType.HEADING)
        md = "###### Heading6"
        self.assertEqual(block_to_block_type(md),BlockType.HEADING)
        # Failed Headings are Paragraphs
        md = "#NotHeading"
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)
        md = "####### NotHeading2"
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        md = "```Code Block Goes Here```"
        self.assertEqual(block_to_block_type(md),BlockType.CODE)
        md = """```
Code Block Goes Here
```"""
        self.assertEqual(block_to_block_type(md),BlockType.CODE)
        # Failed Code Blocks are Paragraphs
        md = "```Not a Code Block``"
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)
        md = """```
Not a Code Block
`"""
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)

    def test_block_to_blocktype_quote(self):
        md = """>Quotestarts
>Quotecontinues
>Quotecontinues
>Quoteends"""
        self.assertEqual(block_to_block_type(md),BlockType.QUOTE)
        md = """>Quotestartsandendshere"""
        self.assertEqual(block_to_block_type(md),BlockType.QUOTE)
        md = """>QuoteStarts
But Abruptly Ends Here"""
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)

    def test_block_to_blocktype_ul(self):
        md = """- This is an unordered list
- and an item here
- and another one here with a few extra newlines below this"""
        self.assertEqual(block_to_block_type(md),BlockType.UNORDERED_LIST)
        md = """- This is a list with one line"""
        self.assertEqual(block_to_block_type(md),BlockType.UNORDERED_LIST)
        md = """- List Starts
But Abruptly Ends Here"""
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)
        md = """-Looks like it should be a list but nah"""
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)

    def test_block_to_blocktype_ol(self):
        md = """1. This is an ordered list
2. With another 
3. With a last item here"""
        self.assertEqual(block_to_block_type(md),BlockType.ORDERED_LIST)
        md = """1. This is an ordered list with only one item"""
        self.assertEqual(block_to_block_type(md),BlockType.ORDERED_LIST)
        md = """1. This is an ordered list
2. With another 
With not a list item here"""
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)
        md = """1.This looks like an ordered list with only one item but nah"""
        self.assertEqual(block_to_block_type(md),BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()