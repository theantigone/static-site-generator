from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(node)
    print(node.text_type)

    html = HTMLNode('h1', 'hello world', 'HTMLNode', {"href": "https://www.google.com"})
    html1 = HTMLNode(props={
    "href": "https://www.google.com",
    "target": "_blank",
    }
                     ).props_to_html()
    print(html)
    print(html1)

    leaf = LeafNode("p", "This is a paragraph of text.").to_html()
    leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
    leaf2 = LeafNode('world cup', 'messi', 'ronaldo')
    print(leaf)
    print(leaf1)
    print(leaf2)

    parent = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(parent.to_html())

    node = TextNode('This is a text node', TextType.TEXT)
    test = text_node_to_html_node(node)
    test1 = node.__repr__()
    print(test)
    print(test1)


if __name__ == "__main__":
    main()
