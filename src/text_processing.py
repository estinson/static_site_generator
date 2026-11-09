from enum import Enum
from textnode import TextNode, TextType

class MarkdownCharacter(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"

def text_to_textnodes(text: str) -> list[TextNode]:
    return_nodes:list[TextNode] = []
    new_origin_node = TextNode(text=text, text_type=TextType.TEXT)
    processing_nodes:list[TextNode] = [new_origin_node]
    for char in [char.value for char in MarkdownCharacter]:
        if char in text:
            processing_nodes = split_nodes_delimiter(processing_nodes, char, TextType[MarkdownCharacter(char).name])
    processing_nodes = split_nodes_image(processing_nodes)
    return_nodes = split_nodes_link(processing_nodes)

    return return_nodes

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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return_nodes:list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        image_tuple = extract_markdown_images(node.text)
        if len(image_tuple) > 0:
            last_image_index_end = 0
            for pair in image_tuple:
                image_index = -1
                if len(pair[0]) > 0 and len(pair[1]) > 0:
                    image_string = f'![{pair[0]}]({pair[1]})'
                    image_index = node.text.find(image_string)
                if image_index >= 0:
                    if image_index != 0:
                        return_nodes.append(TextNode(text=node.text[last_image_index_end:image_index], text_type=TextType.TEXT))
                    last_image_index_end = image_index + len(image_string)
                    return_nodes.append(TextNode(text=pair[0], text_type=TextType.IMAGE, url=pair[1]))
            if last_image_index_end < len(node.text):
                return_nodes.append(TextNode(text=node.text[last_image_index_end:], text_type=TextType.TEXT))
        else:
            return_nodes.append(node)
    return return_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return_nodes:list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        link_tuple = extract_markdown_links(node.text)
        if len(link_tuple) > 0:
            last_link_index_end = 0
            for pair in link_tuple:
                link_index = -1
                if len(pair[0]) > 0 and len(pair[1]) > 0:
                    link_string = f'[{pair[0]}]({pair[1]})'
                    link_index = node.text.find(link_string)
                if link_index >= 0:
                    if link_index != 0:
                        return_nodes.append(TextNode(text=node.text[last_link_index_end:link_index], text_type=TextType.TEXT))
                    last_link_index_end = link_index + len(link_string)
                    return_nodes.append(TextNode(text=pair[0], text_type=TextType.LINK, url=pair[1]))
            if last_link_index_end < len(node.text):
                return_nodes.append(TextNode(text=node.text[last_link_index_end:], text_type=TextType.TEXT))
        else:
            return_nodes.append(node)
    return return_nodes

def extract_markdown_images(text: str) -> list[tuple[str]]:
    rv:list[tuple[str]] = []
    # text: 0, image_start(!):1, alt_text([.+]):2, url((.+)): 3
    mode = 0
    alt_text = None
    url = None
    for i in range(len(text)):
        if text[i] == "!":
            mode = (1 if text[i] == "!" and text[i + 1] == "[" else 0)
        if text[i] == "[" and mode == 1:
            mode = 2
            j = text[i:].find(']')
            alt_text = text[i + 1:i + j] if j > 0 else None
        if mode == 2 and alt_text is not None:
            if text[i] == "(":
                j = text[i:].find(')')
                if j > 0:
                    url = text[i + 1:i + j]
                    rv.append((alt_text, url))
                else:
                    mode = 0
    return rv

def extract_markdown_links(text: str) -> list[tuple[str]]:
    rv:list[tuple[str]] = []
    # text: 0, description([.+]):1, url((.+)): 2
    mode = 0
    description = None
    url = None
    for i in range(len(text)):
        if text[i] == "[" and (text[i - 1] != '!' if i > 0 else True):
            j = text[i:].find(']')
            description = text[i + 1:i + j] if j > 0 else None
            mode = (1 if description else 0)
        if mode == 1 and description is not None:
            if text[i] == "(":
                j = text[i:].find(')')
                if j > 0:
                    url = text[i + 1:i + j]
                    rv.append((description, url))
                else:
                    mode = 0
    return rv
