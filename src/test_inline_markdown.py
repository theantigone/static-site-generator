import unittest

from textnode import *
from inline_markdown import *


class TestInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_non_text(self):
        node = TextNode("**bolded text**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
        [
            TextNode("**bolded text**", TextType.BOLD),
        ])

#    def test_invalid_delimiter(self):
#        node = TextNode("invalid delimiter", TextType.TEXT)
#        with self.assertRaisesRegex(ValueError, 'Delimiter and text type must match: abc and TextType.BOLD are invalid'):
#            split_nodes_delimiter([node], "abc", TextType.BOLD)
#
#    def test_invalid_type(self):
#        node = TextNode("invalid type", TextType.TEXT)
#        with self.assertRaisesRegex(ValueError, 'Delimiter and text type must match: _ and ERROR are invalid'):
#            split_nodes_delimiter([node], "_", 'ERROR')
#
#    def test_wrong_pair(self):
#        node = TextNode("wrong pair", TextType.TEXT)
#        with self.assertRaisesRegex(ValueError, 'Delimiter and text type must match: ` and TextType.ITALIC are invalid'):
#            split_nodes_delimiter([node], "`", TextType.ITALIC)
#
#    def test_both_invalid(self):
#        node = TextNode("invalid type", TextType.TEXT)
#        with self.assertRaisesRegex(ValueError, 'Delimiter and text type must match: ERROR and ERROR are invalid'):
#            split_nodes_delimiter([node], "ERROR", 'ERROR')

    def test_invalid_textnode(self):
        node = TextNode('delimiter', 'type')
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode('delimiter', 'type')])

    def test_entire_text(self):
        node = TextNode("_italic testing_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
        [
            TextNode("italic testing", TextType.ITALIC),
        ])

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_link(self):
        node = TextNode(
            "This is just plain text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just plain text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_image(self):
        node = TextNode(
            "This is just plain text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just plain text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "[link](https://www.example.COM/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.COM/"),
            ],
            new_nodes,
        )

    def test_split_image_with_mixed_nodes_in_list(self):
        nodes = [
            TextNode("Text before. ", TextType.TEXT),
            TextNode("![img1](url1) Some text ![img2](url2)", TextType.TEXT),
            TextNode("This is bold", TextType.BOLD),
            TextNode("Text after ![img3](url3)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text before. ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" Some text ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode("This is bold", TextType.BOLD), # Passed through
                TextNode("Text after ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "url3"),
            ],
            new_nodes
        )

    def test_split_image_at_very_end_of_text(self):
        node = TextNode("Some leading text ![image](url.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some leading text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_text = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_text
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """ 
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "Block 1\n\n\nBlock 2\n\n\n\nBlock 3" # 3 and 4 newlines
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Block 1", "Block 2", "Block 3"]
        )

    def test_markdown_to_blocks_with_whitespace_in_blocks(self):
        md = "  Block 1 has spaces  \n\n  \n  Block 2 also  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Block 1 has spaces", "Block 2 also"] # Individual blocks stripped
        )

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only_input(self):
        md = "   \n \t \n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


    def test_block_to_block_heading(self):
        heading1 = '# This is just a heading'
        heading2 = '## Ths is just a heading'
        heading3 = '### This is just a heading'
        heading4 = '#### This is just a heading'
        heading5 = '##### This is just a heading'
        heading6 = '###### This is just a heading'
        block_type1 = block_to_block_type(heading1)
        block_type2 = block_to_block_type(heading2)
        block_type3 = block_to_block_type(heading3)
        block_type4 = block_to_block_type(heading4)
        block_type5 = block_to_block_type(heading5)
        block_type6 = block_to_block_type(heading6)
        self.assertEqual(block_type1, 'heading')
        self.assertEqual(block_type2, 'heading')
        self.assertEqual(block_type3, 'heading')
        self.assertEqual(block_type4, 'heading')
        self.assertEqual(block_type5, 'heading')
        self.assertEqual(block_type6, 'heading')

    def test_block_to_block_code(self):
        code1 = '```code```'
        code2 = '``` code ```'
        code3 = '''```
            code
            ```'''
        code4 = '''```code
            ```'''
        block_type1 = block_to_block_type(code1)
        block_type2 = block_to_block_type(code2)
        block_type3 = block_to_block_type(code3)
        block_type4 = block_to_block_type(code4)
        self.assertEqual(block_type1, 'code')
        self.assertEqual(block_type2, 'code')
        self.assertEqual(block_type3, 'code')
        self.assertEqual(block_type4, 'code')

    def test_block_to_block_quote(self):
        quote1 = '> quote'
        quote2 = '>  quote'
        quote3 = '>    '
        block_type1 = block_to_block_type(quote1)
        block_type2 = block_to_block_type(quote2)
        block_type3 = block_to_block_type(quote3)
        self.assertEqual(block_type1, 'quote')
        self.assertEqual(block_type2, 'quote')
        self.assertEqual(block_type3, 'quote')

    def test_block_to_block_unordered_list(self):
        unordered_list1 = '- list'
        unordered_list2 = '-  list'
        unordered_list3 = '-    '
        block_type1 = block_to_block_type(unordered_list1)
        block_type2 = block_to_block_type(unordered_list2)
        block_type3 = block_to_block_type(unordered_list3)
        self.assertEqual(block_type1, 'unordered_list')
        self.assertEqual(block_type2, 'unordered_list')
        self.assertEqual(block_type3, 'unordered_list')

    def test_block_to_block_ordered_list(self):
        ordered_list1 = '1. list\n2. d cane\n3. put it down'
        block_type1 = block_to_block_type(ordered_list1)
        self.assertEqual(block_type1, 'ordered_list')

    def test_block_to_block_paragraph(self):
        paragraph1 = 'hello world'
        paragraph2 = ''
        paragraph3 = ' '
        paragraph4 = '```my name jeff'
        paragraph5 = '1  d cane'
        block_type1 = block_to_block_type(paragraph1)
        block_type2 = block_to_block_type(paragraph2)
        block_type3 = block_to_block_type(paragraph3)
        block_type4 = block_to_block_type(paragraph4)
        block_type5 = block_to_block_type(paragraph5)
        self.assertEqual(block_type1, 'paragraph')
        self.assertEqual(block_type2, 'paragraph')
        self.assertEqual(block_type3, 'paragraph')
        self.assertEqual(block_type4, 'paragraph')
        self.assertEqual(block_type5, 'paragraph')


    def test_mixed_line_quote_is_paragraph(self):
        # A true quote block requires ALL lines to start with '>'
        block = "> this is a quote\nthis line is not."
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_unordered_list_with_asterisk(self):
        block = "- An item\n- Another item"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_non_sequential_ordered_list_is_paragraph(self):
        block = "1. First item\n3. Third item" # Skips '2.'
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_embedded_heading_is_paragraph(self):
        block = "This is not a heading\n# But this looks like one"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

1. This is the first list item in a list block
2. This is a list item
3. This is another list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ol><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ol></div>",
        )

    def test_quote_block(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

> This is the first list item in a list block
> This is a list item
> This is another list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><blockquote><p>This is the first list item in a list block This is a list item This is another list item</p></blockquote></div>",
        )

    def test_quote_block(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

> This is the first list item in a list block

Random text here

## hi

### how are you

#### good wbu

##### awesome

###### lol
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><blockquote><p>This is the first list item in a list block</p></blockquote><p>Random text here</p><h2>hi</h2><h3>how are you</h3><h4>good wbu</h4><h5>awesome</h5><h6>lol</h6></div>",
        )


if __name__ == "__main__":
    unittest.main()
