import unittest
from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()
