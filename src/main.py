from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(node)

    html = HTMLNode('h1', 'hello world', 'HTMLNode', {"href": "https://www.google.com"})
    print(html)

if __name__ == "__main__":
    main()
