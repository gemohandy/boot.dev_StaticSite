from textnode import TextNode, TextType
import re

def text_to_textnodes(text):
    first_node = TextNode(text, TextType.PLAIN)
    new_nodes = split_nodes_links([first_node])
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        text_parts = node.text.split(delimiter)
        cur_list = []
        current = False
        for text_part in text_parts:
            cur_list.append(TextNode(text_part, text_type if current else TextType.PLAIN))
            current = not current
        if not current:
            raise Exception("Matching error - odd number of " + delimiter + " in string.")
        new_nodes.extend(cur_list)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)

def split_nodes_image(old_nodes:list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        image_details = extract_markdown_images(node.text)
        if len(image_details) == 0:
            new_nodes.append(node)
            continue
        cur_text = node.text
        for image in image_details:
            middle = f"![{image[0]}]({image[1]})"
            text_parts = cur_text.split(middle)
            if text_parts[0] != "":
                new_nodes.append(TextNode(text_parts[0], TextType.PLAIN))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            cur_text = middle.join(text_parts[1:])
        if cur_text != "":
            new_nodes.append(TextNode(cur_text, TextType.PLAIN))
    return new_nodes
        

def split_nodes_links(old_nodes:list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        link_details = extract_markdown_links(node.text)
        if len(link_details) == 0:
            new_nodes.append(node)
            continue
        cur_text = node.text
        for link in link_details:
            middle = f"[{link[0]}]({link[1]})"
            text_parts = cur_text.split(middle)
            if text_parts[0] != "":
                new_nodes.append(TextNode(text_parts[0], TextType.PLAIN))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            cur_text = middle.join(text_parts[1:])
        if cur_text != "":
            new_nodes.append(TextNode(cur_text, TextType.PLAIN))
    return new_nodes
        