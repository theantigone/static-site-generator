import re

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import *
from enum import Enum


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # 1. Iterate through ALL old nodes
    for old_node in old_nodes:
        # If the node isn't a plain text node, add it and continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # This will hold the results of splitting a single old_node
        split_nodes_for_current_node = []
        
        # 2. No need for a complex 'if'. Split the text directly.
        sections = old_node.text.split(delimiter)
        
        # 3. The check for an unclosed delimiter is still essential
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: unterminated delimiter '{delimiter}'")

        # 4. Loop through the sections from the split
        for i, section_text in enumerate(sections):
            if not section_text: # Skip empty strings (e.g., from '**bold**')
                continue
            
            # Even-indexed sections are plain text
            if i % 2 == 0:
                split_nodes_for_current_node.append(TextNode(section_text, TextType.TEXT))
            # Odd-indexed sections get the new text_type
            else:
                split_nodes_for_current_node.append(TextNode(section_text, text_type))
        
        # 5. Add the newly created nodes to our final list
        new_nodes.extend(split_nodes_for_current_node)

    # 6. Return the final list AFTER the loop is finished
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    # 1. Strip leading/trailing whitespace from the entire document
    stripped_markdown = markdown.strip()
    
    # Handle the case of an empty or whitespace-only input string
    if not stripped_markdown:
        return []
        
    # 2. Split by two or more newlines (which constitute blank lines)
    #    The key here is that .split('\n\n') will create empty strings
    #    if there are more than two newlines.
    raw_blocks = stripped_markdown.split('\n\n')
    
    processed_blocks = []
    for block in raw_blocks:
        # 3. Strip leading/trailing whitespace from each individual block
        cleaned_block = block.strip()
        
        # 4. Filter out any blocks that became empty strings after stripping
        #    This also handles the empty strings created by multiple '\n\n'
        if cleaned_block: # An empty string is "falsey"
            processed_blocks.append(cleaned_block)
            
    return processed_blocks

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown):

    # check for heading
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING.value

    # check for code block
    if markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE.value

    # split line into new lines based on '\n' syntax
    lines = markdown.split('\n')

    # check for quote (every line must start with a '> ')
    if lines and all(line.startswith('>') for line in lines):
        return BlockType.QUOTE.value

    # check for unordered list (every line must start with a '- ')
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST.value

    # check for ordered list (must be sequential, starting from 1)
    if all(line.startswith(f'{i+1}. ') for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST.value

    # if none of the above, it's a paragraph
    return BlockType.PARAGRAPH.value

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        #print(f'CODE ELEMENTS: {[text_node_to_html_node(TextNode(block, TextType.CODE))]}', '\n')
        #block = block.replace('\n', ' ')
        block_type = block_to_block_type(block)
        block_element = markdown_to_html_tags(block, block_type)
        #print(block_element, 'haahahahahaXD\n')
        children.append(block_element)
        #print(f'CHILDREN TO HTML: {ParentNode('div', children).to_html()}', '\n')
    return ParentNode('div', children)

def text_to_children(text):
    leaf_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes

def markdown_to_html_tags(block, block_type):
    match block_type:
        case 'heading':
            if block.startswith('# '):
                block = block.replace('# ', '', 1)
                block_element = ParentNode('h1', text_to_children(block))
            elif block.startswith('## '):
                block = block.replace('## ', '', 1)
                block_element = ParentNode('h2', text_to_children(block))
            elif block.startswith('### '):
                block = block.replace('### ', '', 1)
                block_element = ParentNode('h3', text_to_children(block))
            elif block.startswith('#### '):
                block = block.replace('#### ', '', 1)
                block_element = ParentNode('h4', text_to_children(block))
            elif block.startswith('##### '):
                block = block.replace('##### ', '', 1)
                block_element = ParentNode('h5', text_to_children(block))
            elif block.startswith('###### '):
                block = block.replace('###### ', '', 1)
                block_element = ParentNode('h6', text_to_children(block))
        case 'code':
            content = block
            if content.startswith("```\n"): # Handles ``` followed by newline
                content = content[4:]
            elif content.startswith("```"): # Handles ``` immediately followed by content
                content = content[3:]

            if content.endswith("```"): # Handles content immediately followed by ```
                content = content[:-3]

            block_element = ParentNode('pre', [text_node_to_html_node(TextNode(content, TextType.CODE))])
        case 'quote':
            lines_in_block = block.split('\n')
            #print(lines_in_block)
            cleaned_content_lines = []
            for line in lines_in_block:
                if line.startswith("> "):
                    cleaned_content_lines.append(line[2:]) # Remove "> "
                elif line.startswith(">"): # Handle cases like just ">" on an empty line if needed
                    cleaned_content_lines.append(line[1:]) # Remove ">"
                # If a line doesn't start with ">", block_to_block_type should not have classified it as QUOTE
                # but good to be defensive or assume valid input from previous steps.
            full_quote_content = " ".join(cleaned_content_lines)
            children_nodes = text_to_children(full_quote_content)
            block_element = ParentNode('blockquote', children_nodes)
        case 'unordered_list':
            child_blocks = []
            lines = block.split('\n')
            for line in lines:
                content = ""
                if line.startswith("- "):
                    content = line[2:]
                # block_to_block_type should ensure valid list item format for all lines
                if content or line == "-": # Handle cases like just "-" if that's valid.
                                                     # Usually, content is expected after marker.
                    child_blocks.append(ParentNode('li', text_to_children(content)))
            block_element = ParentNode('ul', child_blocks)
        case 'ordered_list':
            child_blocks = []
            ordered_list = block.split('\n')
            for i, line in enumerate(ordered_list):
                if line.startswith(f'{i+1}. '):
                    cleaned_line = line.replace(f'{i+1}. ', '')
                    # print(text_to_children(cleaned_line))
                    child_blocks.append(ParentNode('li', text_to_children(cleaned_line)))
            block_element = ParentNode('ol', child_blocks)
        case _:
            block = block.replace('\n', ' ')
            block_element = ParentNode('p', text_to_children(block))
    return block_element
