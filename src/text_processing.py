from enum import Enum
from textnode import TextNode, TextType

class MarkdownCharacter(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "["
    IMAGE = "!"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    return_nodes:list[TextNode] = []
    if delimiter not in [char.value for char in MarkdownCharacter]:
        raise ValueError(f'Delimiter is not a recognized markdown character: {delimiter}')
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        split_string:list[str] = node.text.split(delimiter)
        convert:bool = True
        for string in split_string:
            convert = not convert
            if string == '':
                continue

            rv = None
            if convert:
                rv = TextNode(text=string, text_type=text_type)
            else:
                rv = TextNode(text=string, text_type=TextType.TEXT)
            if node.url is not None:
                rv.url = node.url
            return_nodes.append(rv)

        if convert == True and node.text[-1] != delimiter:
            raise ValueError(f'Delimiter: {delimiter} does not have a match after processing')

    return return_nodes
