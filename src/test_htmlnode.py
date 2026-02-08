import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_noattr(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_yesattr(self):
        node = HTMLNode("a", "This is a link", props={"src":"https://google.ca"})
        self.assertEqual(node.props_to_html(), " src=\"https://google.ca\"")

    def test_parent(self):
        node = LeafNode("p", "This is a paragraph")
        node2 = ParentNode("div", children=[node], props={"class": "div_1", "id": "parent"})
        self.assertEqual(node2.to_html(), "<div class=\"div_1\" id=\"parent\"><p>This is a paragraph</p></div>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_attr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_tagless_leaf_to_html(self):
        node = LeafNode(None, "No tag")
        self.assertEqual(node.to_html(), "No tag")
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

if __name__ == "__main__":
    unittest.main()