import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    if delimiter == "":
        raise ValueError("Delimiter cannot be empty")

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown: unmatched delimiter '{delimiter}'"
            )

        for i, section in enumerate(split_text):
            if section == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", text)


def _split_nodes_by_pattern(
    old_nodes: list[TextNode], pattern: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        last_index = 0
        for match in re.finditer(pattern, text):
            if match.start() > last_index:
                new_nodes.append(
                    TextNode(text[last_index:match.start()], TextType.TEXT)
                )
            label, url = match.groups()
            new_nodes.append(TextNode(label, text_type, url))
            last_index = match.end()

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(
        old_nodes, r"!\[([^\]]*)\]\(([^)]*)\)", TextType.IMAGE
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(
        old_nodes, r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", TextType.LINK
    )


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
