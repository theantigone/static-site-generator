import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
