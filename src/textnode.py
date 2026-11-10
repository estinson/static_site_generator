from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "Text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class BlockType(Enum):
    HEADING = "#"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "- "
    ORDERED_NUM_LIST = "1. "
    ORDERED_ALPHA_LIST = "a. "
    PARAGRAPH = ""

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: 'TextNode') -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self) -> str:
        return f'TextNode("{self.text}", {self.text_type}' + (self.url and f', "{self.url}"' or '') + ')'

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(value=text_node.text, tag='b')
        case TextType.ITALIC:
            return LeafNode(value=text_node.text, tag='i')
        case TextType.CODE:
            return LeafNode(value=text_node.text, tag='code')
        case TextType.LINK:
            return LeafNode(value=text_node.text, tag='a', props={'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode(value="", tag='img', props={'alt': text_node.text, 'src': text_node.url})
        case _:
            raise Exception('ERROR: TextType not recognized')
