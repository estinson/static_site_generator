import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_init(self) -> None:
        empty_node = HTMLNode()
        self.assertEqual(empty_node.tag, None)
        self.assertEqual(empty_node.value, None)
        self.assertEqual(empty_node.children, None)
        self.assertEqual(empty_node.props, None)

    def test_props_to_html(self) -> None:
        props_node = LeafNode(
            value="hi",
            props={ "prop_key": "prop_value"},
        )
        self.assertEqual(props_node.props_to_html(), ' prop_key="prop_value"')

    def test_to_html(self) -> None:
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_print(self) -> None:
        child_node = HTMLNode()
        node = HTMLNode(tag="a", value="link", children=[child_node], props={ "props": "values" })
        self.assertEqual(
            node.__repr__(),
            'HTMLNode("a", "link", [HTMLNode("None", "None", None, None)], {\'props\': \'values\'})'
        )

class TestLeafNode(unittest.TestCase):
    def test_leafnode(self) -> None:
        leaf = LeafNode(tag='p', value='Value here!', props={'href':'assets/src'})
        self.assertEqual(leaf.tag, 'p')
        self.assertEqual(leaf.value, 'Value here!')
        self.assertEqual(leaf.props, {'href': 'assets/src'})

    def test_to_html(self) -> None:
        leaf = LeafNode(tag='p', value='Value here!', props={'href':'assets/src'})
        self.assertEqual(leaf.to_html(), '<p href="assets/src">Value here!</p>')

    def test_print(self) -> None:
        leaf = LeafNode(tag='p', value='Value here!', props={'href':'assets/src'})
        self.assertEqual(
            leaf.__repr__(),
            'LeafNode("p", "Value here!", {\'href\': \'assets/src\'})'
        )

    def test_bad_leafnode(self) -> None:
        with self.assertRaises(ValueError):
            LeafNode(value=None, tag='p', props={'href':'assets/src'})

    def test_no_tag_leafnode(self) -> None:
        leaf = LeafNode(value='Value here!', props={'href':'assets/src'})
        self.assertEqual(leaf.to_html(), 'Value here!')

class TestParentNode(unittest.TestCase):
    def test_leafnode(self) -> None:
        parent = ParentNode(
            tag='p',
            children=[
                HTMLNode('p', 'Node'),
                HTMLNode('a', 'PropNode', props={'href':'assets/src'})
            ]
        )
        self.assertEqual(parent.tag, 'p')
        self.assertEqual(parent.value, None)
        self.assertEqual(parent.children[0].props, None)
        self.assertEqual(parent.children[1].props, {'href': 'assets/src'})

    def test_to_html(self) -> None:
        parent = ParentNode(
            tag='p',
            children=[
                LeafNode('Node', 'p'),
                LeafNode('PropNode', 'a', props={'href':'assets/src'})
            ]
        )
        self.assertEqual(
            parent.to_html(),
            '<p><p>Node</p><a href="assets/src">PropNode</a></p>'
        )

    def test_print(self) -> None:
        parent = ParentNode(
            tag='p',
            children=[
                LeafNode('Node', 'p'),
                LeafNode('PropNode', 'a', props={'href':'assets/src'})
            ]
        )
        self.assertEqual(
            parent.__repr__(),
            'ParentNode(\n "p",\n [\n  LeafNode("p", "Node", None),\n  LeafNode("a", "PropNode", {\'href\': \'assets/src\'}),\n ],\n None\n)'
        )

    def test_grandparents(self) -> None:
        parent = ParentNode(
            tag='p',
            children=[
                ParentNode(tag='p', children=[
                    LeafNode('Node', 'p'),
                    LeafNode('PropNode', 'a', props={'href':'assets/src'})
                ])
            ]
        )
        self.assertEqual(
            parent.to_html(),
            '<p><p><p>Node</p><a href="assets/src">PropNode</a></p></p>'
        )

if __name__ == "__main__":
    unittest.main()
