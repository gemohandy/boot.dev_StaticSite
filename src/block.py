from enum import Enum
from htmlnode import LeafNode, ParentNode
from text_to_nodes import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH="paragraph",
    HEADING="heading",
    CODE="code",
    QUOTE="quote",
    UNORDERED="unordered_list",
    ORDERED="ordered_list"

def markdown_to_blocks(markdown:str):
    blocks = markdown.split("\n\n")
    out_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block != "":
            out_blocks.append(new_block)
    return out_blocks

def block_to_block_type(block:str):
    if block[0] == "#":
        for i in range(1,6):
            if(block[i] == " "):
                return BlockType.HEADING
            elif(block[1] == "#"):
                continue
            break
    elif block[0] == "`":
        if block[0:4] == "```\n" and block[-4:] == "\n```":
            return BlockType.CODE
    elif block[0] == ">":
        lines = block.split("\n")
        valid = True
        for line in lines:
            if line[0] != ">":
                valid = False
                break
        if valid:
            return BlockType.QUOTE
    elif block[0] == "-":
        lines = block.split("\n")
        valid = True
        for line in lines:
            if line[0:2] != "- ":
                valid = False
                break
        if valid:
            return BlockType.UNORDERED
    elif block[0] == "1":
        lines = block.split("\n")
        valid = True
        for i in range(0, len(lines)):
            line = lines[i]
            prefix = f"{i+1}. "
            if line[0:len(prefix)] != prefix:
                valid = False
                break
        if valid:
            return BlockType.ORDERED
    return BlockType.PARAGRAPH

def block_to_html_node(block:str, blockType = None):
    if blockType == None:
        blockType = block_to_block_type(block)
    if blockType == BlockType.HEADING:
        prefix = ""
        inner_text = ""
        for i in range(0, 7):
            if block[i] == "#":
                prefix += "#"
            elif block[i] == " ":
                inner_text = block[i+1:]
                break
        inner_nodes = text_to_textnodes(inner_text)
        inner_html = []
        for text_node in inner_nodes:
            inner_html.append(text_node.to_html_node())
        return ParentNode(f"h{len(prefix)}", inner_html)
    if blockType == BlockType.CODE:
        return ParentNode("pre", {LeafNode("code", block[4:-3])})
    if blockType == BlockType.QUOTE:
        lines = block.split("\n")
        text = ""
        for line in lines:
            if len(line) == 1:
                text += "\n"
            elif line[1] == " ":
                text += f"{line[2:]}\n"
            else:
                text += f"{line[1:]}\n"
        inner_nodes = text_to_textnodes(text[:-1])
        inner_html = []
        for text_node in inner_nodes:
            inner_html.append(text_node.to_html_node())
        return ParentNode("blockquote", inner_html)
    if blockType == BlockType.UNORDERED:
        lines = block.split("\n")
        text = ""
        inner_nodes = []
        for line in lines:
            line_nodes = []
            line_text_nodes = text_to_textnodes(line[2:])
            for text_node in line_text_nodes:
                line_nodes.append(text_node.to_html_node())
            inner_nodes.append(ParentNode("li", line_nodes))
        return ParentNode("ul", inner_nodes)
    if blockType == BlockType.ORDERED:
        lines = block.split("\n")
        text = ""
        inner_nodes = []
        for i in range(0, len(lines)):
            line = lines[i]
            prefix = f"{i}. "
            line_nodes = []
            line_text_nodes = text_to_textnodes(line[len(prefix):])
            for text_node in line_text_nodes:
                line_nodes.append(text_node.to_html_node())
            inner_nodes.append(ParentNode("li", line_nodes))
        return ParentNode("ol", inner_nodes)
    one_line = " ".join(block.split("\n"))
    inner_nodes = text_to_textnodes(one_line)
    inner_html = []
    for text_node in inner_nodes:
        inner_html.append(text_node.to_html_node())
    return ParentNode("p", inner_html)
