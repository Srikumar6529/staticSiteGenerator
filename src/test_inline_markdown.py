import unittest
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_delimited_sections(self):
        node = TextNode("**one** and **two** and **three**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("three", TextType.BOLD),
            ],
        )

    def test_split_delimiter_at_start_and_end(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("bold", TextType.BOLD)])

    def test_split_multiple_old_nodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("This is _italic_ text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("This is _italic_ text", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_are_not_split(self):
        bold_node = TextNode("This is **bold** text", TextType.BOLD)
        code_node = TextNode("This is `code`", TextType.CODE)
        new_nodes = split_nodes_delimiter(
            [bold_node, code_node], "**", TextType.BOLD
        )
        self.assertEqual(new_nodes, [bold_node, code_node])

    def test_text_without_delimiter_is_unchanged(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD), [])

    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode("This is **unmatched bold text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_unmatched_delimiter_in_later_node_raises_exception(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("This is _unmatched italic text", TextType.TEXT),
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    def test_empty_delimiter_raises_exception(self):
        node = TextNode("This is plain text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_multiple_markdown_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_image_with_empty_alt_text(self):
        self.assertListEqual(
            [("", "https://www.boot.dev/image.png")],
            extract_markdown_images("![](https://www.boot.dev/image.png)"),
        )

    def test_extract_image_with_empty_url(self):
        self.assertListEqual(
            [("alt text", "")], extract_markdown_images("![alt text]()")
        )

    def test_extract_images_ignores_links(self):
        text = "[to boot dev](https://www.boot.dev)"
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_images_from_mixed_text(self):
        text = (
            "A [link](https://www.boot.dev) and an "
            "![image](https://www.boot.dev/image.png)"
        )
        self.assertListEqual(
            [("image", "https://www.boot.dev/image.png")],
            extract_markdown_images(text),
        )

    def test_extract_images_with_no_matches(self):
        self.assertListEqual(
            [], extract_markdown_images("This is plain text")
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")], matches
        )

    def test_extract_multiple_markdown_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_extract_link_with_empty_anchor_text(self):
        self.assertListEqual(
            [("", "https://www.boot.dev")],
            extract_markdown_links("[](https://www.boot.dev)"),
        )

    def test_extract_link_with_empty_url(self):
        self.assertListEqual(
            [("to boot dev", "")],
            extract_markdown_links("[to boot dev]()"),
        )

    def test_extract_links_ignores_images(self):
        text = "![image](https://www.boot.dev/image.png)"
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_links_from_mixed_text(self):
        text = (
            "A [link](https://www.boot.dev) and an "
            "![image](https://www.boot.dev/image.png)"
        )
        self.assertListEqual(
            [("link", "https://www.boot.dev")],
            extract_markdown_links(text),
        )

    def test_extract_links_with_no_matches(self):
        self.assertListEqual(
            [], extract_markdown_links("This is plain text")
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "Here is ![an image](https://www.boot.dev/image.png) for you",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode(
                    "an image",
                    TextType.IMAGE,
                    "https://www.boot.dev/image.png",
                ),
                TextNode(" for you", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://www.boot.dev/image.png) after",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://www.boot.dev/image.png",
                ),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "before ![image](https://www.boot.dev/image.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://www.boot.dev/image.png",
                ),
            ],
            split_nodes_image([node]),
        )

    def test_split_adjacent_images(self):
        node = TextNode(
            "![one](https://www.boot.dev/1.png)"
            "![two](https://www.boot.dev/2.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://www.boot.dev/1.png"),
                TextNode("two", TextType.IMAGE, "https://www.boot.dev/2.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_duplicate_images(self):
        node = TextNode(
            "![same](https://www.boot.dev/image.png) and "
            "![same](https://www.boot.dev/image.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode(
                    "same", TextType.IMAGE, "https://www.boot.dev/image.png"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "same", TextType.IMAGE, "https://www.boot.dev/image.png"
                ),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_in_multiple_nodes(self):
        nodes = [
            TextNode(
                "first ![one](https://www.boot.dev/1.png)", TextType.TEXT
            ),
            TextNode(
                "second ![two](https://www.boot.dev/2.png)", TextType.TEXT
            ),
        ]
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://www.boot.dev/1.png"),
                TextNode("second ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://www.boot.dev/2.png"),
            ],
            split_nodes_image(nodes),
        )

    def test_split_images_leaves_links_as_text(self):
        node = TextNode(
            "A link [to boot dev](https://www.boot.dev) and "
            "an image ![image](https://www.boot.dev/image.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode(
                    "A link [to boot dev](https://www.boot.dev) and an image ",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://www.boot.dev/image.png",
                ),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_ignores_non_text_nodes(self):
        bold_node = TextNode("bold **text**", TextType.BOLD)
        self.assertListEqual([bold_node], split_nodes_image([bold_node]))

    def test_split_images_with_no_images(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_with_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], split_nodes_image([node]))

    def test_split_images_with_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode(
                    "to boot dev", TextType.LINK, "https://www.boot.dev"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            split_nodes_link([node]),
        )

    def test_split_single_link(self):
        node = TextNode(
            "Here is a [link](https://www.boot.dev) for you",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" for you", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://www.boot.dev) after", TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "before [link](https://www.boot.dev)", TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_adjacent_links(self):
        node = TextNode(
            "[one](https://www.boot.dev/1)[two](https://www.boot.dev/2)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://www.boot.dev/1"),
                TextNode("two", TextType.LINK, "https://www.boot.dev/2"),
            ],
            split_nodes_link([node]),
        )

    def test_split_duplicate_links(self):
        node = TextNode(
            "[same](https://www.boot.dev) and [same](https://www.boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("same", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("same", TextType.LINK, "https://www.boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_in_multiple_nodes(self):
        nodes = [
            TextNode("first [one](https://www.boot.dev/1)", TextType.TEXT),
            TextNode("second [two](https://www.boot.dev/2)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://www.boot.dev/1"),
                TextNode("second ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://www.boot.dev/2"),
            ],
            split_nodes_link(nodes),
        )

    def test_split_links_leaves_images_as_text(self):
        node = TextNode(
            "An image ![image](https://www.boot.dev/image.png) and "
            "a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode(
                    "An image ![image](https://www.boot.dev/image.png) and a link ",
                    TextType.TEXT,
                ),
                TextNode(
                    "to boot dev", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_ignores_non_text_nodes(self):
        italic_node = TextNode("italic _text_", TextType.ITALIC)
        self.assertListEqual([italic_node], split_nodes_link([italic_node]))

    def test_split_links_with_no_links(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_with_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], split_nodes_link([node]))

    def test_split_links_with_empty_list(self):
        self.assertListEqual([], split_nodes_link([]))


class TestTextToTextNodes(unittest.TestCase):
    def test_all_inline_types(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("This is plain text", TextType.TEXT)],
            text_to_textnodes("This is plain text"),
        )

    def test_bold(self):
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("This is **bold** text"),
        )

    def test_italic(self):
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("This is _italic_ text"),
        )

    def test_code(self):
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("This is `code` text"),
        )

    def test_bold_and_italic(self):
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("This is **bold** and _italic_ text"),
        )

    def test_multiple_of_same_type(self):
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" two ", TextType.TEXT),
                TextNode("three", TextType.BOLD),
                TextNode(" four ", TextType.TEXT),
                TextNode("five", TextType.BOLD),
            ],
            text_to_textnodes("**one** two **three** four **five**"),
        )

    def test_image_only(self):
        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://www.boot.dev/image.png",
                )
            ],
            text_to_textnodes(
                "![image](https://www.boot.dev/image.png)"
            ),
        )

    def test_link_only(self):
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://www.boot.dev")],
            text_to_textnodes("[link](https://www.boot.dev)"),
        )

    def test_multiple_images_and_links(self):
        text = (
            "![one](https://www.boot.dev/1.png) "
            "[two](https://www.boot.dev/2) "
            "![three](https://www.boot.dev/3.png) "
            "[four](https://www.boot.dev/4)"
        )
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://www.boot.dev/1.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://www.boot.dev/2"),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "three", TextType.IMAGE, "https://www.boot.dev/3.png"
                ),
                TextNode(" ", TextType.TEXT),
                TextNode("four", TextType.LINK, "https://www.boot.dev/4"),
            ],
            text_to_textnodes(text),
        )

    def test_formatting_without_surrounding_text(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            text_to_textnodes("**bold**_italic_`code`"),
        )

    def test_empty_text(self):
        self.assertListEqual([], text_to_textnodes(""))


if __name__ == "__main__":
    unittest.main()
