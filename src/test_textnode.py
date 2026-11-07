import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        link_node = TextNode("This is not a text node", TextType.LINK)
        image_node = TextNode("This is not a text node", TextType.IMAGE, 'assets/image')
        self.assertNotEqual(image_node, link_node)
        self.assertEqual(image_node.text, link_node.text)
        self.assertNotEqual(image_node.url, None)
        self.assertEqual(link_node.url, None)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type.value, TextType.BOLD.value)

if __name__ == "__main__":
    unittest.main()
