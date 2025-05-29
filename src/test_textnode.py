import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.CODE, None)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_url_diff(self):
        node = TextNode("This is a text node", TextType.LINK, 'https://www.bing.com')
        node2 = TextNode("This is a text node", TextType.LINK, 'https://www.google.com')
        self.assertNotEqual(node, node2)

    def test_text_diff(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is another text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode('abc', TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'abc')
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode('abc', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'abc')
        self.assertEqual(html_node.props, None)
        
    def test_code(self):
        node = TextNode('abc', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'abc')
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode('abc', TextType.LINK, 'https://www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'abc')
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode('abc', TextType.IMAGE, 'https://www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "abc"})

    def test_invalid(self):
        node = TextNode('abc', 'Joseph P Marsh', 'https://www.google.com')
        with self.assertRaisesRegex(ValueError, 'TextNode requires a valid type: Joseph P Marsh is invalid'):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
