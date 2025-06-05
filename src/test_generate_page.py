import unittest

from main import *

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        header = extract_title('hello_world.md')
        self.assertEqual(header, 'Hello World')

    def test_no_header(self):
        with self.assertRaisesRegex(ValueError, 'no h1 header'):
            extract_title('no_header.md')


if __name__ == "__main__":
    unittest.main()
