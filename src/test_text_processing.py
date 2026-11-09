import unittest
from text_processing import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
    markdown_to_blocks
)
from textnode import TextNode, TextType

# NOTE:
# Debugging commands for testing out all node results while writing
# print()
# [print(node) for node in new_nodes]

class TestMarkdownToBlocks(unittest.TestCase):
    def test_it_works(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items
"""
        result = markdown_to_blocks(markdown)
        self.assertEqual(len(result), 3)

class TestTextToTextNode(unittest.TestCase):
    def test_it_works(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertEqual(len(new_nodes), 10)

        self.assertEqual(
            [new_nodes[0].text_type, new_nodes[0].text], [TextType.TEXT, 'This is ']
        )
        self.assertEqual(
            [new_nodes[1].text_type, new_nodes[1].text], [TextType.BOLD, 'text']
        )
        self.assertEqual(
            [new_nodes[2].text_type,new_nodes[2].text], [TextType.TEXT, ' with an ']
        )
        self.assertEqual(
            [new_nodes[3].text_type, new_nodes[3].text], [TextType.ITALIC, 'italic']
        )
        self.assertEqual(
            [new_nodes[4].text_type, new_nodes[4].text], [TextType.TEXT, ' word and a ']
        )
        self.assertEqual(
            [new_nodes[5].text_type, new_nodes[5].text], [TextType.CODE, 'code block']
        )
        self.assertEqual(
            [new_nodes[6].text_type, new_nodes[6].text], [TextType.TEXT, ' and an ']
        )
        self.assertEqual(
            [new_nodes[7].text_type, new_nodes[7].text, new_nodes[7].url],
            [TextType.IMAGE, 'obi wan image', 'https://i.imgur.com/fJRm4Vk.jpeg']
        )
        self.assertEqual(
            [new_nodes[8].text_type, new_nodes[8].text], [TextType.TEXT, ' and a ']
        )
        self.assertEqual(
            [new_nodes[9].text_type, new_nodes[9].text, new_nodes[9].url],
            [TextType.LINK, 'link', 'https://boot.dev']
        )

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_code_text_node(self):
        old_nodes:list[TextNode] = [
            TextNode("This is a text node with `code within it` and text after it", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        old_nodes:list[TextNode] = [
            TextNode("`code at the start of it` and text after it", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

        old_nodes:list[TextNode] = [
            TextNode("Text at the start of it `code at the end of it`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_multiple_formatting(self):
        old_nodes:list[TextNode] = [
            TextNode("This is a **text node** with `code within it` and text after it", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual('*' in new_nodes[0].text, True)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        newest_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
        self.assertEqual(len(newest_nodes), 5)
        self.assertEqual(newest_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(newest_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(newest_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(newest_nodes[3].text_type, TextType.CODE)
        self.assertEqual(newest_nodes[4].text_type, TextType.TEXT)

    def test_failed_markdown(self):
        old_nodes:list[TextNode] = [TextNode("Bold text malformed**", TextType.TEXT)]

        try:
            new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
        except (ValueError) as e:
            self.assertEqual('does not have a match' in str(e), True)

        old_nodes:list[TextNode] = [TextNode("*Bold text malformed*", TextType.TEXT)]

        try:
            new_nodes = split_nodes_delimiter(old_nodes, '*', TextType.BOLD)
        except (ValueError) as e:
            self.assertEqual('not a recognized markdown character' in str(e), True)

class TestSplitNodeImage(unittest.TestCase):
    def test_it_works(self):
        old_nodes:list[TextNode] = [
            TextNode("This is a text node with ![an image](within/it) and text after it", TextType.TEXT),
            TextNode("![an image](within/it) and text after it", TextType.TEXT),
            TextNode("This is a text node with ![an image](within/it)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual(len(new_nodes), 7)

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is a text node with ")

        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, 'an image')
        self.assertEqual(new_nodes[1].url, 'within/it')

        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, ' and text after it')

        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, 'an image')
        self.assertEqual(new_nodes[3].url, 'within/it')

        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, ' and text after it')

        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "This is a text node with ")

        self.assertEqual(new_nodes[6].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[6].text, 'an image')
        self.assertEqual(new_nodes[6].url, 'within/it')

class TestSplitNodeLink(unittest.TestCase):
    def test_it_works(self):
        old_nodes:list[TextNode] = [
            TextNode("This is a text node with [a link](within/it) and text after it", TextType.TEXT),
            TextNode("[a link](within/it) and text after it", TextType.TEXT),
            TextNode("This is a text node with [a link](within/it)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)

        self.assertEqual(len(new_nodes), 7)

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is a text node with ")

        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, 'a link')
        self.assertEqual(new_nodes[1].url, 'within/it')

        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, ' and text after it')

        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, 'a link')
        self.assertEqual(new_nodes[3].url, 'within/it')

        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, ' and text after it')

        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "This is a text node with ")

        self.assertEqual(new_nodes[6].text_type, TextType.LINK)
        self.assertEqual(new_nodes[6].text, 'a link')
        self.assertEqual(new_nodes[6].url, 'within/it')

class TestExtractMarkdownImages(unittest.TestCase):
    def test_it_works(self):
        text = "This is text with an ![image](asset/src)"
        processed = extract_markdown_images(text)
        self.assertEqual(processed, [('image', 'asset/src')])

    def test_it_doesnt(self):
        text = "This is text with almost an ![image](asset/src"
        processed = extract_markdown_images(text)
        self.assertEqual(processed, [])

        text = "This is text with almost an ![image(asset/src)"
        processed = extract_markdown_images(text)
        self.assertEqual(processed, [])

        text = "This is text with almost an [image](asset/src)"
        processed = extract_markdown_images(text)
        self.assertEqual(processed, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_it_works(self):
        text = "This is text with a [link](asset/src)"
        processed = extract_markdown_links(text)
        self.assertEqual(processed, [('link', 'asset/src')])

    def test_it_doesnt(self):
        text = "This is text with almost an ![link](asset/src)"
        processed = extract_markdown_links(text)
        self.assertEqual(processed, [])

        text = "This is text with almost an [link(asset/src)"
        processed = extract_markdown_links(text)
        self.assertEqual(processed, [])

        text = "This is text with almost an [link](asset/src"
        processed = extract_markdown_links(text)
        self.assertEqual(processed, [])
