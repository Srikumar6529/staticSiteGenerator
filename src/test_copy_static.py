import os
import tempfile
import unittest

from main import copy_static


class TestCopyStatic(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source = os.path.join(self.temp_dir.name, "static")
        self.destination = os.path.join(self.temp_dir.name, "public")
        os.makedirs(os.path.join(self.source, "images"))

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_file(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def test_copies_files_and_nested_directories(self):
        self.write_file(
            os.path.join(self.source, "index.css"), "body {}"
        )
        self.write_file(
            os.path.join(self.source, "images", "tolkien.png"), "image data"
        )

        copy_static(self.source, self.destination)

        self.assertEqual(
            self.read_file(os.path.join(self.destination, "index.css")),
            "body {}",
        )
        self.assertEqual(
            self.read_file(
                os.path.join(self.destination, "images", "tolkien.png")
            ),
            "image data",
        )

    def test_deletes_existing_destination_contents(self):
        os.makedirs(self.destination)
        self.write_file(
            os.path.join(self.destination, "stale.txt"), "stale content"
        )
        self.write_file(os.path.join(self.source, "index.css"), "body {}")

        copy_static(self.source, self.destination)

        self.assertFalse(
            os.path.exists(os.path.join(self.destination, "stale.txt"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.destination, "index.css"))
        )

    def test_copies_multiple_nested_levels(self):
        self.write_file(
            os.path.join(self.source, "a", "b", "c", "file.txt"), "deep"
        )

        copy_static(self.source, self.destination)

        self.assertEqual(
            self.read_file(
                os.path.join(
                    self.destination, "a", "b", "c", "file.txt"
                )
            ),
            "deep",
        )


if __name__ == "__main__":
    unittest.main()
