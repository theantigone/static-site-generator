import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html = HTMLNode("p", "text")
        html2 = HTMLNode("p", "text")
        self.assertEqual(html, html2)

    def test_neq(self):
        html = HTMLNode("a", "text")
        html2 = HTMLNode("h1", "text")
        self.assertNotEqual(html, html2)

    def test_eq_props_to_html_value(self):
        html = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        html2 = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertEqual(html, html2)

    def test_neq_props_to_html_value(self):
        html = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        html2 = HTMLNode(None, None, None, {"href": "https://www.bing.com"})
        self.assertNotEqual(html, html2)

    def test_neq_props_to_html_key(self):
        html = HTMLNode(None, None, None, {"href": "https://www.bing.com"})
        html2 = HTMLNode(None, None, None, {"target": "https://www.bing.com"})
        self.assertNotEqual(html, html2)

    def test_neq_props_to_html_empty(self):
        html = HTMLNode()
        html2 = HTMLNode(None, None, None, {"target": "https://www.bing.com"})
        self.assertNotEqual(html, html2)

    # Example test case for your unittest suite
    def test_props_to_html_with_none_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    # Example test case
    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    # New test cases for populated props output
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_to_html_multiple_props(self):
        # Python 3.7+ dictionaries preserve insertion order.
        # If older Python or uncertain order, a more complex check might be needed
        # (e.g., splitting the string and checking for presence of each attribute).
        # For most learning contexts, assuming insertion order is fine.
        node = HTMLNode(props={"alt": "My Awesome Image", "src": "image.png"})
        self.assertEqual(node.props_to_html(), ' alt="My Awesome Image" src="image.png"')
        
    def test_props_to_html_props_with_various_values(self):
        node = HTMLNode(props={"data-id": "123", "class": "text-bold main-content"})
        self.assertEqual(node.props_to_html(), ' data-id="123" class="text-bold main-content"')


if __name__ == "__main__":
    unittest.main()
