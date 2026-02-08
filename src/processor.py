from htmlnode import HTMLNode, LeafNode, ParentNode
from block import markdown_to_blocks, block_to_block_type, block_to_html_node, BlockType

def markdown_to_html_node(markdown:str):
    blocks_text = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks_text:
        block_nodes.append(block_to_html_node(block))
    outer_node = ParentNode("div", block_nodes)
    return outer_node