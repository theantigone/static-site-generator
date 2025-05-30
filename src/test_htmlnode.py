import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )


    def leaf_test_eq(self):
        leaf = LeafNode("p", "text")
        leaf2 = LeafNode("p", "text")
        self.assertEqual(leaf, leaf2)

    def leaf_test_neq(self):
        leaf = LeafNode("a", "text")
        leaf2 = LeafNode("h1", "text")
        self.assertNotEqual(leaf, leaf2)

    def test_eq_props_value(self):
        leaf = LeafNode("h1", "hi", {"href": "https://www.google.com"})
        leaf2 = LeafNode("h1", "hi", {"href": "https://www.google.com"})
        self.assertEqual(leaf, leaf2)

    def test_neq_props_value(self):
        leaf = LeafNode("h2", "bye", {"href": "https://www.google.com"})
        leaf2 = LeafNode("h2", "bye", {"href": "https://www.bing.com"})
        self.assertNotEqual(leaf, leaf2)

    def test_neq_props_key(self):
        leaf = LeafNode("h3", "hello", {"href": "https://www.bing.com"})
        leaf2 = LeafNode("h3", "hello", {"target": "https://www.bing.com"})
        self.assertNotEqual(leaf, leaf2)

    def test_value_error_if_value_is_none(self):
        node_without_value = LeafNode('p', None)
        with self.assertRaisesRegex(ValueError, 'LeafNode requires a value.'):
            node_without_value.to_html()

   # 2. Test for raw text output (no tag)
    def test_to_html_no_tag_returns_raw_value(self): # Renamed for clarity
        leaf = LeafNode(None, 'Hello World') # tag is None by default
        # Corrected assertion:
        self.assertEqual(leaf.to_html(), 'Hello World')

    # 3. Tests for HTML output with tags
    def test_to_html_with_tag_and_value(self): # Renamed for clarity
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_tag_value_and_props(self): # Renamed for clarity
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_tag_value_and_empty_props(self):
        # Test that empty props are handled correctly (no extra space or "{}")
        node = LeafNode("p", "Text with empty props.", {})
        self.assertEqual(node.to_html(), "<p>Text with empty props.</p>")
        
    def test_to_html_with_tag_value_and_none_props(self):
        node = LeafNode("p", "Text with None props.", None) # Props is None by default too
        self.assertEqual(node.to_html(), "<p>Text with None props.</p>")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # 1. Refine __eq__ tests to compare objects, not HTML strings
    def test_eq_parent_node_object_equality(self): # Renamed for clarity
        child_node1 = LeafNode('h1', 'child')
        child_node2 = LeafNode('h1', 'child') # Identical to child_node1
        parent_node1 = ParentNode('h2', [child_node1], {"class": "main"})
        parent_node2 = ParentNode('h2', [child_node2], {"class": "main"})
        # This now tests your ParentNode.__eq__ method directly
        self.assertEqual(parent_node1, parent_node2)

    def test_neq_parent_node_due_to_child_value(self): # Renamed
        child_node1 = LeafNode('h1', 'child')
        child_node2 = LeafNode('h1', 'orphan') # Different value
        parent_node1 = ParentNode('h2', [child_node1])
        parent_node2 = ParentNode('h2', [child_node2])
        self.assertNotEqual(parent_node1, parent_node2)

    def test_neq_parent_node_due_to_child_tag(self): # Renamed
        child_node1 = LeafNode('h1', 'child')
        child_node2 = LeafNode('h3', 'child') # Different tag
        parent_node1 = ParentNode('h2', [child_node1])
        parent_node2 = ParentNode('h2', [child_node2])
        self.assertNotEqual(parent_node1, parent_node2)

    def test_neq_parent_node_due_to_parent_tag(self):
        child_node = LeafNode('h1', 'child')
        parent_node1 = ParentNode('h2', [child_node])
        parent_node2 = ParentNode('div', [child_node]) # Different parent tag
        self.assertNotEqual(parent_node1, parent_node2)

    def test_none_tag_value_error(self):
        child_node = LeafNode('span', 'child')
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, 'ParentNode requires a tag.'):
            parent_node.to_html()

    def test_none_children_value_error(self):
        child_node = LeafNode('span', 'child')
        parent_node = ParentNode('div', None)
        with self.assertRaisesRegex(ValueError, 'ParentNode requires a child.'):
            parent_node.to_html()

    # 2. Add ValueError test for empty children list
    def test_empty_children_list_value_error(self):
        parent_node = ParentNode(tag='div', children=[]) # children is an empty list
        with self.assertRaisesRegex(ValueError, 'ParentNode requires a child.'): # Adjusted message
            parent_node.to_html()

    def test_to_html_child_props(self):
        child_node = LeafNode('span', 'child', {'href': 'https://www.google.com'})
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span href="https://www.google.com">child</span></div>'
        )

    def test_to_html_parent_props(self):
        child_node = LeafNode('span', 'child')
        parent_node = ParentNode('div', [child_node], {'href': 'https://www.bing.com'})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.bing.com"><span>child</span></div>'
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
