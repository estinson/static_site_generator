from text_processing import (
    text_to_textnodes, markdown_to_blocks, block_to_block_type,
)
from textnode import (
    TextNode, TextType, BlockType,
    text_node_to_html_node,
)
from htmlnode import HTMLNode, ParentNode, LeafNode

def markdown_to_html(markdown: str) -> HTMLNode:
    debug:bool = False
    blocks:list[str] = markdown_to_blocks(markdown)
    html_blocks:list[HTMLNode] = []
    for block in blocks:
        block_type:BlockType = block_to_block_type(block)
        new_node:HTMLNode = None
        match block_type:
            case BlockType.HEADING:
                header_count = [string.rindex(block_type.value) + 1 for string  in block.split('\n')][0]
                html_blocks.append(
                    ParentNode(
                        tag=f'h{header_count}',
                        children=block_text_to_html(
                            text=[string[header_count + 1:] for string in block.split('\n')]
                        )
                    )
                )
            case BlockType.CODE:
                html_blocks.append(
                    ParentNode(tag='pre', children=block_text_to_html(text="\n".join(block.split("\n")[1:-1]), tag='code'))
                )
            case BlockType.QUOTE:
                html_blocks.append(
                    ParentNode(
                        tag='blockquote',
                        children=block_text_to_html(
                            text=[string[len(block_type.value) + 1:] for string in block.split('\n')],
                        )
                    )
                )
            case BlockType.UNORDERED_LIST:
                html_blocks.append(
                    ParentNode(
                        tag='ul',
                        children=block_text_to_html(
                            text=[string[len(block_type.value):] for string in block.split('\n')],
                            tag='li'
                        )
                    )
                )
            case BlockType.ORDERED_NUM_LIST:
                html_blocks.append(
                    ParentNode(
                        tag='ol',
                        children=block_text_to_html(
                            text=[string[len(block_type.value):] for string in block.split('\n')],
                            tag='li'
                        ),
                    )
                )
            case BlockType.ORDERED_ALPHA_LIST:
                html_blocks.append(
                    ParentNode(
                        tag='ol',
                        children=block_text_to_html(
                            text=[string[len(block_type.value):] for string in block.split('\n')],
                            tag='li',
                        ),
                        props={'type': "a"}
                    )
                )
            case BlockType.PARAGRAPH:
                html_blocks.append(
                    ParentNode(
                        tag='p',
                        children=block_text_to_html(
                            text=[string[len(block_type.value):] for string in block.split('\n')],
                        )
                    )
                )
            case _:
                raise ValueError('ERROR(markdown_to_html): BlockType failed!')
        if debug: print(f'Added {block_type.name} to html_blocks:\n{html_blocks[-1]}')
        if new_node is not None:
            html_blocks.append(new_node)
    return ParentNode(tag='div', children=html_blocks)

def block_text_to_html(text:list[str], tag:str = None) -> list[HTMLNode]:
    list_return:list[HTMLNode] = []
    if tag == 'code':
        return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

    for string in text:
        nodes = [text_node_to_html_node(node) for node in text_to_textnodes(string)]
        if tag:
            nodes = [ParentNode(tag=tag, children=nodes)]
        list_return += nodes
    return list_return
