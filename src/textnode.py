from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    IMAGE = "image"
    LINK = "link"
class TextNode:

    def __init__(self, text: str, text_type: TextType, url: None | str = None ):

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:

        if self.text != other.text:
            return False
        if self.text_type.value != other.text_type.value:
            return False
        return self.url == other.url

    def __repr__(self):
        
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
