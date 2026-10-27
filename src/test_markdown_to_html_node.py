import unittest
from block_markdown import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
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

    def test_codeblock_does_not_parse_inline_markdown(self):
        md = """```
**bold** _italic_ `code` [link](https://boot.dev)
```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>**bold** _italic_ `code` [link](https://boot.dev)\n</code></pre></div>",
        )

    def test_heading(self):
        node = markdown_to_html_node("# This is a **heading**")
        self.assertEqual(
            node.to_html(), "<div><h1>This is a <b>heading</b></h1></div>"
        )

    def test_all_heading_levels(self):
        md = "\n\n".join(f"{'#' * level} Heading {level}" for level in range(1, 7))
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "<h4>Heading 4</h4>"
            "<h5>Heading 5</h5>"
            "<h6>Heading 6</h6>"
            "</div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a blockquote</blockquote></div>",
        )

    def test_blockquote_without_space_after_marker(self):
        node = markdown_to_html_node(">This is a quote")
        self.assertEqual(
            node.to_html(), "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_blockquote_with_inline_markdown(self):
        md = """
> This is **bold**
> and _italic_ text
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is <b>bold</b> and <i>italic</i> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a **bold** item
- This is an _italic_ item
- This is a `code` item
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>This is a <b>bold</b> item</li><li>This is an <i>italic</i> item</li><li>This is a <code>code</code> item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second **bold** item
3. Third _italic_ item
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First item</li><li>Second <b>bold</b> item</li><li>Third <i>italic</i> item</li></ol></div>",
        )

    def test_paragraph_with_inline_link(self):
        md = "This is a [link](https://boot.dev) in a paragraph"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>This is a <a href="https://boot.dev">link</a> in a paragraph</p></div>',
        )

    def test_mixed_blocks(self):
        md = """# Heading

A paragraph with **bold** text.

> A quote

- one
- two

1. first
2. second

```
raw **code**
```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Heading</h1>"
            "<p>A paragraph with <b>bold</b> text.</p>"
            "<blockquote>A quote</blockquote>"
            "<ul><li>one</li><li>two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<pre><code>raw **code**\n</code></pre>"
            "</div>",
        )

    def test_empty_markdown(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")

    def test_returns_parent_div(self):
        node = markdown_to_html_node("A paragraph")
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)


if __name__ == "__main__":
    unittest.main()
