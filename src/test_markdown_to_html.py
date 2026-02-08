import unittest

from processor import markdown_to_html_node


class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_all(self):
        md = """
# This is a heading

### This is a smaller heading

####### This is NOT a heading - too many pound signs

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

This is a paragraph with [a link](https://google.ca) and an ![image](https://i.imgur.com/zjjcJKZ.png)

- This is a list
- with items

1. This is an ordered list.
2. It's items are in order.

> This is a quote

```
This is code
```
"""
        expected_output = "<div><h1>This is a heading</h1><h3>This is a smaller heading</h3><p>####### This is NOT a heading - too many pound signs</p><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here This is the same paragraph on a new line</p><p>This is a paragraph with <a href=\"https://google.ca\">a link</a> and an <img src=\"https://i.imgur.com/zjjcJKZ.png\" alt=\"image\"></img></p><ul><li>This is a list</li><li>with items</li></ul><ol><li>This is an ordered list.</li><li>It's items are in order.</li></ol><quote>This is a quote</quote><pre><code>This is code\n</code></pre></div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, expected_output)