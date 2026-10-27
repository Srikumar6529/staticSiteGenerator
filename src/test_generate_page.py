import os
import tempfile
import unittest

from main import extract_title, generate_page, generate_pages_recursive


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello there   "), "Hello there")

    def test_extract_title_from_larger_document(self):
        markdown = """Some text before

# My Page Title

Some text after
"""
        self.assertEqual(extract_title(markdown), "My Page Title")

    def test_extract_title_returns_first_h1(self):
        markdown = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_extract_title_ignores_h2_and_below(self):
        markdown = "## Not the title\n\n### Also not the title"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_without_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("This is just a paragraph.")


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_file(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def test_generate_page_replaces_title_and_content(self):
        from_path = os.path.join(self.root, "index.md")
        template_path = os.path.join(self.root, "template.html")
        dest_path = os.path.join(self.root, "public", "index.html")

        self.write_file(
            from_path,
            "# My Page\n\nThis is **bold** and _italic_ text.",
        )
        self.write_file(
            template_path,
            "<title>{{ Title }}</title><article>{{ Content }}</article>",
        )

        generate_page(from_path, template_path, dest_path, "/")

        self.assertEqual(
            self.read_file(dest_path),
            "<title>My Page</title><article><div><h1>My Page</h1>"
            "<p>This is <b>bold</b> and <i>italic</i> text.</p></div>"
            "</article>",
        )

    def test_generate_page_creates_missing_directories(self):
        from_path = os.path.join(self.root, "index.md")
        template_path = os.path.join(self.root, "template.html")
        dest_path = os.path.join(
            self.root, "nested", "public", "index.html"
        )

        self.write_file(from_path, "# Title\n\nContent")
        self.write_file(
            template_path, "{{ Title }}: {{ Content }}"
        )

        generate_page(from_path, template_path, dest_path, "/")

        self.assertTrue(os.path.exists(dest_path))

    def test_generate_page_overwrites_existing_file(self):
        from_path = os.path.join(self.root, "index.md")
        template_path = os.path.join(self.root, "template.html")
        dest_path = os.path.join(self.root, "index.html")

        self.write_file(from_path, "# Title\n\nNew content")
        self.write_file(template_path, "{{ Content }}")
        self.write_file(dest_path, "Old content")

        generate_page(from_path, template_path, dest_path, "/")

        self.assertIn("New content", self.read_file(dest_path))
        self.assertNotIn("Old content", self.read_file(dest_path))

    def test_generate_page_prefixes_root_relative_links_with_basepath(self):
        from_path = os.path.join(self.root, "index.md")
        template_path = os.path.join(self.root, "template.html")
        dest_path = os.path.join(self.root, "index.html")

        self.write_file(
            from_path,
            "# Title\n\n[Home](/)\n\n![Image](/images/image.png)",
        )
        self.write_file(
            template_path,
            '<link href="/index.css" rel="stylesheet" />'
            "<a href=\"/\">Home</a>"
            "{{ Content }}",
        )

        generate_page(
            from_path, template_path, dest_path, "/staticSiteGenerator/"
        )

        html = self.read_file(dest_path)
        self.assertIn(
            'href="/staticSiteGenerator/index.css"', html
        )
        self.assertIn('href="/staticSiteGenerator/"', html)
        self.assertIn(
            'src="/staticSiteGenerator/images/image.png"', html
        )

    def test_generate_pages_recursive_creates_matching_structure(self):
        content_dir = os.path.join(self.root, "content")
        template_path = os.path.join(self.root, "template.html")
        dest_dir = os.path.join(self.root, "public")

        self.write_file(
            os.path.join(content_dir, "index.md"),
            "# Home\n\nHome content",
        )
        self.write_file(
            os.path.join(content_dir, "blog", "post", "index.md"),
            "# Blog Post\n\nBlog content",
        )
        self.write_file(
            os.path.join(content_dir, "contact", "index.md"),
            "# Contact\n\nContact content",
        )
        self.write_file(template_path, "{{ Title }}|{{ Content }}")

        generate_pages_recursive(content_dir, template_path, dest_dir, "/")

        self.assertTrue(
            os.path.exists(os.path.join(dest_dir, "index.html"))
        )
        self.assertTrue(
            os.path.exists(
                os.path.join(dest_dir, "blog", "post", "index.html")
            )
        )
        self.assertTrue(
            os.path.exists(os.path.join(dest_dir, "contact", "index.html"))
        )

        blog_html = self.read_file(
            os.path.join(dest_dir, "blog", "post", "index.html")
        )
        self.assertIn("Blog Post", blog_html)
        self.assertIn("<h1>Blog Post</h1>", blog_html)

    def test_generate_pages_recursive_ignores_non_markdown_files(self):
        content_dir = os.path.join(self.root, "content")
        template_path = os.path.join(self.root, "template.html")
        dest_dir = os.path.join(self.root, "public")

        self.write_file(
            os.path.join(content_dir, "index.md"),
            "# Home\n\nContent",
        )
        self.write_file(
            os.path.join(content_dir, "notes.txt"), "Not markdown"
        )
        self.write_file(template_path, "{{ Content }}")

        generate_pages_recursive(content_dir, template_path, dest_dir, "/")

        self.assertTrue(
            os.path.exists(os.path.join(dest_dir, "index.html"))
        )
        self.assertFalse(
            os.path.exists(os.path.join(dest_dir, "notes.html"))
        )
        self.assertFalse(
            os.path.exists(os.path.join(dest_dir, "notes.txt"))
        )


if __name__ == "__main__":
    unittest.main()
