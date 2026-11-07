import unittest
from text_processing import split_nodes_delimiter
from textnode import TextNode, TextType

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
