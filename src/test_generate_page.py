import unittest
import os
import shutil
import tempfile

# --- Functions from main.py (or stubs) needed for generate_page ---

def extract_title(markdown_path):
    with open(markdown_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('# '):
                return line[2:] # Simpler extraction
    raise ValueError('no h1 header')

# --- Mock/Stub for markdown_to_html_node dependency ---
class MockHTMLNode:
    def __init__(self, html_content):
        self.html_content = html_content

    def to_html(self):
        return self.html_content

def markdown_to_html_node(markdown_string):
    """
    Simplified stub for testing generate_page.
    In a real scenario, this would be your actual Markdown to HTML converter.
    """
    # Example: convert "**bold**" to "<b>bold</b>" and wrap in <p>
    processed_html = markdown_string.replace("**bold**", "<b>bold</b>")
    processed_html = processed_html.replace("_italic_", "<i>italic</i>")
    return MockHTMLNode(f"<div>{processed_html}</div>") # Ensure it returns a common structure
# --- End Mocks/Stubs ---

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    with open(from_path, 'r') as f_markdown:
        markdown_content = f_markdown.read()
    
    with open(template_path, 'r') as f_template:
        template_content = f_template.read()
    
    html_content_from_markdown = markdown_to_html_node(markdown_content).to_html()
    
    title = "" # Default title
    try:
        title = extract_title(from_path)
    except ValueError as e:
        print(f"Warning: Could not extract title from {from_path}: {e}. Using default or empty title.")
        # Decide how to handle this: use a default, leave empty, or re-raise if critical
        # For this example, we'll proceed with an empty title if not found, 
        # but your requirements might differ.

    # Perform replacements
    final_html = template_content.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html_content_from_markdown)
    
    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir): # Check if dest_dir is not empty
        print(f"Creating directory: {dest_dir}")
        os.makedirs(dest_dir)
        
    with open(dest_path, 'w') as f_dest:
        f_dest.write(final_html)
    print(f"Page generated: {dest_path}")

# --- Test Class ---

class TestGeneratePage(unittest.TestCase):

    def setUp(self):
        """
        Set up temporary directories and files for testing.
        This method is called before each test method.
        """
        # Create a temporary directory to hold all test files
        self.test_dir = tempfile.mkdtemp() 
        
        # Define paths for our test source files and destination
        self.src_content_dir = os.path.join(self.test_dir, "content")
        self.template_dir = os.path.join(self.test_dir, "templates")
        self.dest_public_dir = os.path.join(self.test_dir, "public")

        os.makedirs(self.src_content_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)
        # No need to create self.dest_public_dir here, generate_page should do it.

        # Create a sample markdown file
        self.sample_md_path = os.path.join(self.src_content_dir, "sample.md")
        with open(self.sample_md_path, "w") as f:
            f.write("# My Awesome Page\n\nThis is **bold** and _italic_ content.")

        # Create another markdown file without a H1 title
        self.no_title_md_path = os.path.join(self.src_content_dir, "notitle.md")
        with open(self.no_title_md_path, "w") as f:
            f.write("Just some paragraph text.\nNo H1 here.")
        
        # Create an empty markdown file
        self.empty_md_path = os.path.join(self.src_content_dir, "empty.md")
        with open(self.empty_md_path, "w") as f:
            f.write("")

        # Create a sample template file
        self.sample_template_path = os.path.join(self.template_dir, "base.html")
        with open(self.sample_template_path, "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

    def tearDown(self):
        """
        Clean up temporary directories and files.
        This method is called after each test method, even if the test fails.
        """
        shutil.rmtree(self.test_dir)

    def test_basic_page_generation(self):
        """Test generating a page with title and content."""
        dest_file_path = os.path.join(self.dest_public_dir, "output.html")
        generate_page(self.sample_md_path, self.sample_template_path, dest_file_path)

        self.assertTrue(os.path.exists(dest_file_path)) # Check if file was created

        with open(dest_file_path, "r") as f:
            generated_content = f.read()
        
        expected_html_content = markdown_to_html_node("# My Awesome Page\n\nThis is **bold** and _italic_ content.").to_html()
        expected_output = f"<html><head><title>My Awesome Page</title></head><body>{expected_html_content}</body></html>"
        self.assertEqual(generated_content, expected_output)

    def test_page_generation_with_subdir_creation(self):
        """Test if destination subdirectories are created."""
        dest_file_path = os.path.join(self.dest_public_dir, "subdir", "nested_page.html")
        generate_page(self.sample_md_path, self.sample_template_path, dest_file_path)

        self.assertTrue(os.path.exists(dest_file_path))
        
        with open(dest_file_path, "r") as f:
            generated_content = f.read()

        expected_html_content = markdown_to_html_node("# My Awesome Page\n\nThis is **bold** and _italic_ content.").to_html()
        expected_output = f"<html><head><title>My Awesome Page</title></head><body>{expected_html_content}</body></html>"
        self.assertEqual(generated_content, expected_output)

    def test_generate_page_when_md_has_no_h1_title(self):
        """Test page generation when markdown file lacks an H1 title."""
        dest_file_path = os.path.join(self.dest_public_dir, "no_title_page.html")
        
        # generate_page now has a try-except for extract_title
        generate_page(self.no_title_md_path, self.sample_template_path, dest_file_path)
        
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, "r") as f:
            generated_content = f.read()

        # Content from notitle.md, processed by our stub markdown_to_html_node
        md_content_no_title = "Just some paragraph text.\nNo H1 here."
        expected_html_content = markdown_to_html_node(md_content_no_title).to_html()
        
        # Title will be empty as per our modified generate_page
        expected_output = f"<html><head><title></title></head><body>{expected_html_content}</body></html>"
        self.assertEqual(generated_content, expected_output)

    def test_generate_page_with_empty_markdown(self):
        """Test page generation with an empty markdown file."""
        dest_file_path = os.path.join(self.dest_public_dir, "empty_content_page.html")
        
        # extract_title will raise ValueError on an empty file if no H1 is found
        # The modified generate_page will catch this and use an empty title.
        generate_page(self.empty_md_path, self.sample_template_path, dest_file_path)
        
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, "r") as f:
            generated_content = f.read()

        expected_html_content = markdown_to_html_node("").to_html() # Empty content
        expected_output = f"<html><head><title></title></head><body>{expected_html_content}</body></html>"
        self.assertEqual(generated_content, expected_output)

    def test_generate_page_template_placeholders_not_in_template(self):
        """Test behavior if template doesn't have placeholders."""
        simple_template_path = os.path.join(self.template_dir, "simple_template.html")
        with open(simple_template_path, "w") as f:
            f.write("<html><body>Static Content Only</body></html>")

        dest_file_path = os.path.join(self.dest_public_dir, "static_template_page.html")
        generate_page(self.sample_md_path, simple_template_path, dest_file_path)
        
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, "r") as f:
            generated_content = f.read()
        
        # The content should be exactly the template, as replacements won't occur
        expected_output = "<html><body>Static Content Only</body></html>"
        self.assertEqual(generated_content, expected_output)

if __name__ == "__main__":
    unittest.main()
