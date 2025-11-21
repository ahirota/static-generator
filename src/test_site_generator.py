import unittest

from site_generator import extract_title

class TestSiteGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is a header


This is a paragraph with an extra new line above this 
This is the same paragraph on a new line






- This is a list with EXCESSIVE newlines above this
- and an item here
- and another one here with a few extra newlines below this



"""
        title = extract_title(md)
        self.assertEqual("This is a header", title)

    def test_extract_title_multiple(self):
        md = """
This is a paragraph 
This is the same paragraph on a new line

# This is the first header

# This is the second header

- This is a list
- and an item here
- and another one here
"""
        title = extract_title(md)
        self.assertEqual("This is the first header", title)

    def test_extract_title_failed(self):
        md = """
## This is an h2

### This is an h3

#this is a paragraph that looks like an h1

"""
        with self.assertRaises(Exception):
            extract_title(md)
        



if __name__ == "__main__":
    unittest.main()