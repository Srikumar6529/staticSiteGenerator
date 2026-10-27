import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def copy_static(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    _copy_directory(source, destination)


def _copy_directory(source: str, destination: str) -> None:
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            print(f"Creating directory {destination_path}")
            os.mkdir(destination_path)
            _copy_directory(source_path, destination_path)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[1:].strip()
    raise ValueError("Markdown does not contain an h1 heading")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    destination_directory = os.path.dirname(dest_path)
    if destination_directory:
        os.makedirs(destination_directory, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str,
) -> None:
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                html_destination_path = os.path.splitext(destination_path)[0] + ".html"
                generate_page(
                    source_path,
                    template_path,
                    html_destination_path,
                    basepath,
                )
        else:
            generate_pages_recursive(
                source_path, template_path, destination_path, basepath
            )


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
