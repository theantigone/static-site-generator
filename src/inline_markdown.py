import re

from textnode import TextNode, TextType


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

def _split_nodes_generic(old_nodes, extract_function, new_node_type, markdown_format_string):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text_to_process = old_node.text
        extracted_items = extract_function(text_to_process)

        if not extracted_items:
            new_nodes.append(old_node)
            continue

        for item_tuple in extracted_items: # e.g., (alt_text, url) or (link_text, url)
            text_content, url = item_tuple

            # Reconstruct the exact markdown delimiter string
            delimiter = markdown_format_string.format(text_content=text_content, url=url)

            sections = text_to_process.split(delimiter, 1)

            # If the delimiter (reconstructed from extracted item) isn't found,
            # it implies an issue or that the text_to_process has been exhausted
            # in a way that removed this item. The solution's error here is one way.
            # For this exercise, if extract_function guarantees items are present,
            # this error should ideally not be hit with valid, non-overlapping markdown.
            if len(sections) != 2:
                raise ValueError(f"Invalid markdown, {new_node_type.value} section not found for '{delimiter}'")

            # Add text before the current item, if any:
            # checks if sections[0] is not an empty string
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Add the image/link node
            new_nodes.append(TextNode(text_content, new_node_type, url))

            # Continue processing with the remainder of the text
            text_to_process = sections[1]

        # Add any remaining text after the last item:
        # appends the original text (if it were entirely plain text) from the
        # beginning to the new_nodes list
        if text_to_process:
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    return _split_nodes_generic(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        "![{text_content}]({url})" # Format string for image markdown
    )

def split_nodes_link(old_nodes):
    return _split_nodes_generic(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        "[{text_content}]({url})" # Format string for link markdown
    )

