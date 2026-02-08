import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("Alt Text", TextType.IMAGE, "LINKTOIMAGE")
        self.assertEqual(node.to_html_node().to_html(), "<img src=\"LINKTOIMAGE\" alt=\"Alt Text\"></img>")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://google.ca")
        self.assertEqual(node.to_html_node().to_html(), "<a href=\"https://google.ca\">Click me!</a>")