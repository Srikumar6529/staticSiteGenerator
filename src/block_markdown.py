import re
from enum import Enum

from parentnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def _is_ordered_list(lines: list[str]) -> bool:
    for expected_number, line in enumerate(lines, start=1):
        match = re.match(r"^(\d+)\. ", line)
        if match is None or int(match.group(1)) != expected_number:
            return False
    return True


def text_to_children(text: str) -> list:
    return [
        text_node_to_html_node(text_node)
        for text_node in text_to_textnodes(text)
    ]


def _paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def _heading_to_html_node(block: str) -> ParentNode:
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def _code_to_html_node(block: str) -> ParentNode:
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    code_node = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code_node])


def _quote_to_html_node(block: str) -> ParentNode:
    lines = []
    for line in block.split("\n"):
        lines.append(line.removeprefix(">").strip())
    return ParentNode("blockquote", text_to_children(" ".join(lines)))


def _unordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def _ordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = re.sub(r"^\d+\. ", "", line, count=1)
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(_paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(_heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(_code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(_quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(_unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(_ordered_list_to_html_node(block))

    return ParentNode("div", children)
