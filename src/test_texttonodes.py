from textnode import TextNode, TextType
from text_to_nodes import split_nodes_delimiter,text_to_textnodes

import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_nontext(self):
        bold_node = TextNode("Bold _italic_ bold", TextType.BOLD)
        italic_node = TextNode("Italics _extra_ italics", TextType.ITALIC)
        code_node = TextNode("Code _italics_ code", TextType.CODE)
        link_node = TextNode("Link _italic_ link", TextType.LINK, "https://google.ca")
        image_node = TextNode("Image _italic_ image", TextType.IMAGE, "https://image")
        nodes = [bold_node, italic_node, code_node, link_node, image_node]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), nodes)

    def test_bold(self):
        new_nodes = text_to_textnodes("Text **bold** text")
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " text")

    def test_italic(self):
        new_nodes = text_to_textnodes("Text _italic_ text")
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " text")

    def test_code(self):
        new_nodes = text_to_textnodes("Text `code` text")
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " text")

    def test_many(self):
        new_nodes = text_to_textnodes("Text **bold** **bold** **bold** text")
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[4].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[4].text, " ")
        self.assertEqual(new_nodes[5].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[5].text, "bold")
        self.assertEqual(new_nodes[6].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[6].text, " text")

    def test_all(self):
        new_nodes = text_to_textnodes("Text **bold** `code` _italic_ text")
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Text ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[4].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[4].text, " ")
        self.assertEqual(new_nodes[5].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[5].text, "italic")
        self.assertEqual(new_nodes[6].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[6].text, " text")

        
    def test_broken(self):
        try:
            new_nodes = text_to_textnodes("Text _ita")
        except Exception as e:
            self.assertEqual(repr(e), "Exception('Matching error - odd number of _ in string.')")

    def test_extract_markdown_images(self):
        new_nodes = text_to_textnodes("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
    
    def test_images(self):
        new_nodes = text_to_textnodes("This is text with two ![images](https://i.imgur.com/zjjcJKZ.png) ![secondImage](https://link)")
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "This is text with two ")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, "images")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, "secondImage")
        self.assertEqual(new_nodes[3].url, "https://link")

    def test_links(self):
        new_nodes = text_to_textnodes("This is [text](https://google.ca) with two [links](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].url, "https://google.ca")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " with two ")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, "links")
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_image_links(self):
        new_nodes = text_to_textnodes("This is [text](https://google.ca) with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].url, "https://google.ca")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, " with an ")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, "image")
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/zjjcJKZ.png")
    
