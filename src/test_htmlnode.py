import unittest
from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = HtmlNode(props)
        node2 = HtmlNode(props)
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test1(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = HtmlNode(props)
        node2 = HtmlNode(props)
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test2(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node1 = HtmlNode(props)
        node2 = HtmlNode(props)
        self.assertEqual(node1.props_to_html(), node2.props_to_html())





if __name__ == "__main__":
    unittest.main()
