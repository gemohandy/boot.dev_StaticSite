from textnode import TextNode, TextType
import os
import shutil
import sys
from processor import markdown_to_html_node

def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    copyDirectory("static/", "docs/")
    generate_page_recursive(basepath, "content/", "template.html", "docs/")

def copyDirectory(source, destination):
    if(os.path.exists(destination)):
        shutil.rmtree(destination)
    copyDirectoryRecursive(source, destination)

def copyDirectoryRecursive(source, destination):
    os.mkdir(destination)
    sub_items = os.listdir(source)
    for item in sub_items:
        full_name = os.path.join(source, item)
        target_name = os.path.join(destination, item)
        if os.path.isfile(full_name):
            shutil.copy(full_name, target_name)
        else:
            copyDirectoryRecursive(full_name, target_name)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0:2] == "# ":
            return line[2:]
    raise Exception("No title found")

def generate_page_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    sub_items = os.listdir(dir_path_content)
    for item in sub_items:
        full_name = os.path.join(dir_path_content, item)
        target_name = os.path.join(dest_dir_path, item)
        if os.path.isfile(full_name):
            if(full_name[-3:] == ".md"):
                generate_page(basepath, full_name, template_path, target_name[:-3] + ".html")
        else:
            generate_page_recursive(basepath, full_name, template_path, target_name)


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    markdown = file.read()
    template_file = open(template_path)
    template = template_file.read()
    inner_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", inner_html)
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")
    output_file = open(dest_path, "w")
    output_file.write(template)

main()