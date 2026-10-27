import unittest
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_paragraph_and_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("This is a single block"), ["This is a single block"]
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n  \n\n\t"), [])

    def test_leading_and_trailing_newlines(self):
        md = "\n\nThis is a block\n\n"
        self.assertEqual(markdown_to_blocks(md), ["This is a block"])

    def test_excessive_newlines_between_blocks(self):
        md = "First block\n\n\n\n\nSecond block"
        self.assertEqual(
            markdown_to_blocks(md), ["First block", "Second block"]
        )

    def test_blank_lines_containing_whitespace(self):
        md = "First block\n\n   \n\nSecond block"
        self.assertEqual(
            markdown_to_blocks(md), ["First block", "Second block"]
        )

    def test_strips_leading_and_trailing_whitespace(self):
        md = "   First block   \n\n\tSecond block\t"
        self.assertEqual(
            markdown_to_blocks(md), ["First block", "Second block"]
        )

    def test_single_newlines_are_preserved(self):
        md = "Line one\nLine two\n\nAnother block\nStill the same block"
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Line one\nLine two",
                "Another block\nStill the same block",
            ],
        )

    def test_multiple_blocks(self):
        md = "One\n\nTwo\n\nThree\n\nFour"
        self.assertEqual(
            markdown_to_blocks(md), ["One", "Two", "Three", "Four"]
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."),
            BlockType.PARAGRAPH,
        )

    def test_heading_levels(self):
        for level in range(1, 7):
            block = f"{'#' * level} Heading {level}"
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block), BlockType.HEADING
                )

    def test_heading_with_seven_hashes_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Too many hashes"),
            BlockType.PARAGRAPH,
        )

    def test_heading_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("#No space after hash"),
            BlockType.PARAGRAPH,
        )

    def test_heading_with_text_containing_hashes(self):
        self.assertEqual(
            block_to_block_type("## Heading with # inside"),
            BlockType.HEADING,
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_multiline_code_block(self):
        block = "```\ndef hello():\n    print('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_blank_lines(self):
        block = "```\nline one\n\nline three\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_empty_code_block(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)

    def test_code_without_newline_after_backticks_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("```print('hello')```"),
            BlockType.PARAGRAPH,
        )

    def test_code_without_closing_backticks_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')"), BlockType.PARAGRAPH
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> This is a quote"), BlockType.QUOTE
        )

    def test_quote_without_space_after_marker(self):
        self.assertEqual(
            block_to_block_type(">This is a quote"), BlockType.QUOTE
        )

    def test_multiline_quote(self):
        block = "> First line\n> Second line\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_multiline_quote_with_mixed_spacing(self):
        block = "> First line\n>Second line\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_missing_marker_is_paragraph(self):
        block = "> First line\nSecond line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- First item"), BlockType.UNORDERED_LIST
        )

    def test_multiline_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(
            block_to_block_type(block), BlockType.UNORDERED_LIST
        )

    def test_unordered_list_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("-First item"), BlockType.PARAGRAPH
        )

    def test_unordered_list_missing_marker_is_paragraph(self):
        block = "- First item\nSecond item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. First item"), BlockType.ORDERED_LIST
        )

    def test_multiline_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(
            block_to_block_type(block), BlockType.ORDERED_LIST
        )

    def test_ordered_list_must_start_at_one(self):
        block = "2. First item\n3. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        block = "1. First item\n3. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_not_repeat_number(self):
        block = "1. First item\n1. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1.First item"), BlockType.PARAGRAPH
        )

    def test_ordered_list_with_parenthesis_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1) First item"), BlockType.PARAGRAPH
        )

    def test_ordered_list_missing_number_is_paragraph(self):
        block = "1. First item\nSecond item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_with_many_items(self):
        block = "\n".join(f"{i}. Item {i}" for i in range(1, 12))
        self.assertEqual(
            block_to_block_type(block), BlockType.ORDERED_LIST
        )

    def test_empty_block_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
