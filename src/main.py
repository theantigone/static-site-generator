from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import *

import os
import shutil
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
    # Ensure basepath starts and ends with a slash if it's not just "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/") and basepath != "/":
        basepath = basepath + "/"
else:
    basepath = "/" # Default for root deployment

def src_to_dst(src, dst):
    print(f"Copying content from '{src}' to '{dst}'") # Informative print

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")
    if not os.path.isdir(src):
        raise NotADirectoryError(f"Source '{src}' is not a directory.")

    # Ensure the destination is a clean, empty directory
    if os.path.exists(dst):
        print(f"Destination '{dst}' exists. Removing it to ensure a clean copy.")
        shutil.rmtree(dst)
    
    print(f"Creating destination directory '{dst}'.")
    os.mkdir(dst) # Use makedirs; it's fine even if only creating one level

    # Get full paths of items in the source directory
    src_item_names = os.listdir(src)
    src_item_full_paths = []
    for name in src_item_names:
        src_item_full_paths.append(os.path.join(src, name))
    
    # Initiate the recursive copy
    recursively_search_directory(src_item_full_paths, src, dst)
    print("Copy complete.")
    # No explicit return needed unless specified by requirements for testing

# Your recursively_search_directory
def recursively_search_directory(src_list, src, dst):
    for file_path in src_list: # 'file' renamed to 'file_path' for clarity
        if os.path.isfile(file_path):
            print(f'copying {file_path} to {dst}') # Debug print
            shutil.copy(file_path, dst) # Copies file into dst directory
        elif os.path.isdir(file_path):
            # Calculate corresponding destination directory path
            # 'file_path' is like /path/to/src/subdir
            # 'src' is like /path/to/src
            # 'dst' is like /path/to/dst_root
            # We want to create /path/to/dst_root/subdir
            target_subdir_name = os.path.basename(file_path) # Gets 'subdir'
            new_dst_dir = os.path.join(dst, target_subdir_name) # Creates /path/to/dst_root/subdir

            # Your original way using replace also works for this specific structure:
            # new_dst_dir_alt = file_path.replace(src, dst) 
            # This is fine as long as 'src' is a unique prefix.

            print(f'creating directory {new_dst_dir}') # Debug print
            os.makedirs(new_dst_dir) # Create the destination subdirectory

            # Get items inside the current source subdirectory
            subdir_item_names = os.listdir(file_path)
            subdir_item_full_paths = []
            for name in subdir_item_names:
                subdir_item_full_paths.append(os.path.join(file_path, name))
            
            print(f'recursively searching through {new_dst_dir} now') # Debug print
            # Recursive call:
            # src_list: items in current source subdir
            # src: current source subdir path (file_path)
            # dst: new destination subdir path (new_dst_dir)
            recursively_search_directory(subdir_item_full_paths, file_path, new_dst_dir)
        else:
            # This case is for items that are neither a file nor a directory
            # (e.g., broken symlinks, special files).
            # Raising an error might be too strict; often, these are just skipped.
            print(f"Warning: Item '{file_path}' is neither a file nor a directory. Skipping.")
            # raise ValueError(f'Item {file_path} is not a file or directory.')
    # return os.listdir(dst) # This returns contents of the *current* dst dir being processed.
                           # Not typically useful in a recursive copy.

def extract_title(markdown):
    with open(markdown, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('# '):
                return line[2:] # Slice the string after "# "
    raise ValueError('no h1 header')

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    print(f'converting {from_path} to list')
    with open(from_path, 'r') as f:
        markdown = f.read()
    print(f'converting {template_path} to list')
    with open(template_path, 'r') as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(from_path)

    # Assuming template_content is the full template string
    final_html_content = template.replace('{{ Title }}', title)
    final_html_content = final_html_content.replace('{{ Content }}', html)
    final_html_content = final_html_content.replace('href="/', f'href="{basepath}')
    final_html_content = final_html_content.replace('src="/', f'src="{basepath}')

    html_filename = os.path.basename(dest_path)
    directory_path = os.path.dirname(dest_path)
    if directory_path and not os.path.exists(directory_path):
        os.makedirs(directory_path)
    with open(dest_path, 'w') as fp:
        fp.write(final_html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Processing directory: {dir_path_content}") # Helpful for debugging
    src_dir_list = os.listdir(dir_path_content)
    for item_name in src_dir_list: # Changed 'src_path' to 'item_name' for clarity
        full_src_path = os.path.join(dir_path_content, item_name)
        
        if os.path.isdir(full_src_path):
            # This is a subdirectory in the content folder
            print(f"Found subdirectory: {item_name}")
            
            # Path for the source subdirectory (this is full_src_path)
            # src_subdir_to_recurse = full_src_path # No need for src_path_joined

            # Path for the corresponding destination subdirectory
            dest_subdir_for_recursion = os.path.join(dest_dir_path, item_name)
            
            # CRITICAL: Create the destination subdirectory if it doesn't exist
            # This needs to happen *before* you try to put files in it or recurse into it
            print(f"Ensuring destination subdirectory exists: {dest_subdir_for_recursion}")
            os.makedirs(dest_subdir_for_recursion, exist_ok=True) 
            
            # Recursive call
            generate_pages_recursive(full_src_path, template_path, dest_subdir_for_recursion, basepath)
            
        elif os.path.isfile(full_src_path):
            # This is a file in the content folder
            print(f"Found file: {item_name}")
            
            # BUG 1 & 2 & 3: The logic below is incorrect.
            # It ignores the actual file found (full_src_path / item_name)
            # and always tries to process "index.md".
            # It also doesn't check if the file is a Markdown file.

            # --- CORRECTED FILE HANDLING LOGIC ---
            if item_name.endswith(".md"): # Process only Markdown files
                # Determine the output HTML filename (change .md to .html)
                base_name_without_ext, _ = os.path.splitext(item_name)
                output_html_filename = base_name_without_ext + ".html"
                
                # Construct the full destination path for the HTML file
                # It should go into the current dest_dir_path
                full_dest_html_path = os.path.join(dest_dir_path, output_html_filename)
                
                print(f"Generating page for Markdown file: {full_src_path}")
                print(f"  Output HTML will be: {full_dest_html_path}")
                
                # Call your existing generate_page function
                # generate_page(source_markdown_path, template_file_path, destination_html_path)
                generate_page(full_src_path, template_path, full_dest_html_path, basepath)
            else:
                print(f"Skipping non-Markdown file: {item_name}")
                # Optionally, you could copy other static files here if needed,
                # but the lesson usually separates static asset copying.
            # --- END OF CORRECTED FILE HANDLING LOGIC ---
            
        else:
            # This handles cases like broken symlinks or other special file types
            print(f"Warning: Item '{item_name}' in '{dir_path_content}' is neither a file nor a directory. Skipping.")
            
    # No return value is typically needed for a function that performs actions like this

def main():
#    node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
#    print(node)
#    print(node.text_type)
#
#    html = HTMLNode('h1', 'hello world', 'HTMLNode', {"href": "https://www.google.com"})
#    html1 = HTMLNode(props={
#    "href": "https://www.google.com",
#    "target": "_blank",
#    }
#                     ).props_to_html()
#    print(html)
#    print(html1)
#
#    leaf = LeafNode("p", "This is a paragraph of text.").to_html()
#    leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
#    leaf2 = LeafNode('world cup', 'messi', 'ronaldo')
#    print(leaf)
#    print(leaf1)
#    print(leaf2)
#
#    parent = ParentNode(
#        "p",
#        [
#            LeafNode("b", "Bold text"),
#            LeafNode(None, "Normal text"),
#            LeafNode("i", "italic text"),
#            LeafNode(None, "Normal text"),
#        ],
#    )
#
#    print(parent.to_html())
#
#    node = TextNode('This is a text node', TextType.TEXT)
#    test = text_node_to_html_node(node)
#    test1 = node.__repr__()
#    print(test)
#    print(test1)
#
#    node = TextNode("This is text with a `code block` word", TextType.TEXT)
#    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#    print(new_nodes, '\n')
#
#    node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
#    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#    print(new_nodes, '\n')
#
#    node = TextNode(
#        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#        TextType.TEXT,
#    )
#    new_nodes = split_nodes_link([node])
#    # [
#    #     TextNode("This is text with a link ", TextType.TEXT),
#    #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#    #     TextNode(" and ", TextType.TEXT),
#    #     TextNode(
#    #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#    #     ),
#    # ]
#    print(new_nodes, '\n')
#
#    node = TextNode(
#        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#        TextType.TEXT,
#    )
#    new_nodes = split_nodes_image([node])
#    print(new_nodes, '\n')
#
#
#    node = TextNode(
#        "![image](https://www.example.COM/IMAGE.PNG)",
#        TextType.TEXT,
#    )
#    new_nodes = split_nodes_image([node])
#    print(new_nodes, '\n')
#
#
#    text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
#
#    new_text = text_to_textnodes(text)
#    print(new_text, '\n')
#
#    md = '''
## This is a heading
#
#This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
#
#> This is the first list item in a list block
#> This is a list item
#> This is another list item
#'''
#
#    blocks = markdown_to_blocks(md)
#    print(blocks, '\n')
#    print(markdown_to_html_node(md).to_html(), '\n')
#
#    md = """
#This is **bolded** paragraph
#text in a p
#tag here
#
#This is another paragraph with _italic_ text and `code` here
#
#"""
#
#    # joseph = markdown_to_blocks(md)
#    node = markdown_to_html_node(md)
#    html = node.to_html()
#    print(html, '\n')
#    # print(joseph, '\n')
#
#    md = """
## This is a heading
#
#This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
#
#> This is the first list item in a list block
#
#Random text here
#
### hi
#
#### how are you
#
##### good wbu
#
###### awesome
#
####### lol
#"""
#
#    # print(f'JOHNNY APPLE SEED: {joseph}', '\n')
#    # john = markdown_to_blocks(md)
#    node = markdown_to_html_node(md)
#    html = node.to_html()
#    print(html)
#    # print(john)
#    # print(f'HELLO: {node}', '\n')
#    # print(f'DIE: [{text_node_to_html_node(TextNode(md, TextType.CODE))}]', '\n')

#    md = '''
## Tolkien Fan Club
#
#![JRR Tolkien sitting](/images/tolkien.png)
#
#Here's the deal, **I like Tolkien**.
#
#> "I am in fact a Hobbit in all but size."
#>
#> -- J.R.R. Tolkien
#'''
#
#    blocks = markdown_to_blocks(md)
#    print(blocks, '\n')
#    print(markdown_to_html_node(md).to_html(), '\n')
#
#    print(src_to_dst('static/', 'public/'))
#    print(generate_page('content/index.md', 'template.html', 'public/index.html'))

    src_to_dst('static/', 'docs/')
#    generate_page('content/index.md', 'template.html', 'public/index.html')
#    generate_page('content/blog/glorfindel/index.md', 'template.html', 'public/blog/glorfindel/index.html')
#    generate_page('content/blog/tom/index.md', 'template.html', 'public/blog/tom/index.html')
#    generate_page('content/blog/majesty/index.md', 'template.html', 'public/blog/majesty/index.html')
#    generate_page('content/contact/index.md', 'template.html', 'public/contact/index.html')
    generate_pages_recursive('content', 'template.html', 'docs', basepath)


if __name__ == "__main__":
    main()
