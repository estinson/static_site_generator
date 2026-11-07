from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main() -> None:
    node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    htmlnode = HTMLNode(tag="a", value="link", props={ "props": "values" })
    print(node)
    print(htmlnode)

if __name__ == "__main__":
    main()
