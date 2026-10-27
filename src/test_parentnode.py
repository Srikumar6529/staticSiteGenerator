import unittest
from leafnode import LeafNode
from parentnode import ParentNode


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

    def test_to_html_with_no_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )

    def test_to_html_with_props_on_nested_nodes(self):
        node = ParentNode(
            "div",
            [ParentNode("span", [LeafNode("b", "text")], {"class": "inner"})],
            {"class": "outer"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="outer"><span class="inner"><b>text</b></span></div>',
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "ul",
                            [
                                ParentNode("li", [LeafNode(None, "one")]),
                                ParentNode("li", [LeafNode(None, "two")]),
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><ul><li>one</li><li>two</li></ul></section></div>",
        )

    def test_to_html_with_no_tag_raises_value_error(self):
        node = ParentNode(None, [LeafNode(None, "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_no_children_raises_value_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag_and_no_children_raises_value_error(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_value_is_none(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.value)

    def test_constructor_requires_tag_and_children(self):
        with self.assertRaises(TypeError):
            ParentNode()
        with self.assertRaises(TypeError):
            ParentNode("div")


if __name__ == "__main__":
    unittest.main()
