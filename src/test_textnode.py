import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test1(self):
        node1 = TextNode("testnode1", TextType.BOLD)
        node2 = TextNode("testnode2", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test2(self):
        node1 = TextNode("testnode1", TextType.LINK)
        node2 = TextNode("testnode2", TextType.LINK)
        self.assertNotEqual(node1, node2)
    
    def test3(self):
        node1 = TextNode("testnode", TextType.LINK, "link1")
        node2 = TextNode("testnode", TextType.LINK, "link2")
        self.assertNotEqual(node1, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")
        self.assertEqual(html_node.to_html(), "<code>This is code</code>")

    def test_link(self):
        node = TextNode(
            "This is a link", TextType.LINK, "https://www.boot.dev"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.boot.dev">This is a link</a>',
        )

    def test_image(self):
        node = TextNode(
            "This is an image", TextType.IMAGE, "https://www.boot.dev/image.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://www.boot.dev/image.png",
                "alt": "This is an image",
            },
        )

    def test_invalid_text_type_raises_exception(self):
        node = TextNode("This is invalid", "not a text type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()
