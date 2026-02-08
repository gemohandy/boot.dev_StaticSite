import unittest

from block import markdown_to_blocks, block_to_block_type, BlockType


class TestTextNode(unittest.TestCase):
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

    def test_all_block_types(self):
        md = """
# This is a heading

### This is a smaller heading

####### This is NOT a heading - too many pound signs

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. This is an ordered list.
2. It's items are in order.

> This is a quote

```
This is code
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "### This is a smaller heading",
                "####### This is NOT a heading - too many pound signs",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",     
                "1. This is an ordered list.\n2. It's items are in order.",
                "> This is a quote",
                "```\nThis is code\n```"
            ],
        )
        expectedTypes = [BlockType.HEADING,
                         BlockType.HEADING,
                         BlockType.PARAGRAPH,
                         BlockType.PARAGRAPH,
                         BlockType.PARAGRAPH,
                         BlockType.UNORDERED,
                         BlockType.ORDERED,
                         BlockType.QUOTE,
                         BlockType.CODE]
        actualTypes = []
        for i in range(0, len(blocks)):
            self.assertEqual(block_to_block_type(blocks[i]), expectedTypes[i])

    def test_extra_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items








Lots of new lines before this paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "Lots of new lines before this paragraph"
            ],
        )