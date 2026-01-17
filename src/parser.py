from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes : list[TextNode], delimiter : str, text_type : TextType) -> list[TextNode]:
    result_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_node_list.append(old_node)
            continue
        list_sub_node = old_node.text.split(delimiter)
        if len(list_sub_node) % 2 == 0:
            raise ValueError("Missing closing delimiter")
        for index, sub_node_text in enumerate(list_sub_node):
            if index % 2 == 0:
                result_node_list.append(TextNode(sub_node_text, old_node.text_type))
            else:
                result_node_list.append(TextNode(sub_node_text, text_type))
    return result_node_list

def extract_markdown_images(text : str) -> list[tuple[str]]:
    return re.findall(r"\!\[([^\]]+)\]\(([^\)]+)\)", text)

def extract_markdown_link(text : str) -> list[tuple[str]]:
    return re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", text)

def split_nodes_link(old_nodes : list[TextNode]) -> list[TextNode]:
    result_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_node_list.append(old_node)
            continue
        text = old_node.text
        while len(text) > 0:
            match_text = re.search(r"(?<!\!)\[([^\]]+)\]\(([^\)]+)\)", text)
            if match_text is not None:
                result_node_list.append(TextNode(text[:match_text.start()], old_node.text_type))
                result_node_list.append(TextNode(match_text.group(1), TextType.LINK, match_text.group(2)))
                text = text[match_text.end():]
            else:
                result_node_list.append(TextNode(text, old_node.text_type))
                text = ""
    return result_node_list

def split_nodes_image(old_nodes : list[TextNode]) -> list[TextNode]:
    result_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_node_list.append(old_node)
            continue
        text = old_node.text
        while len(text) > 0:
            match_text = re.search(r"\!\[([^\]]+)\]\(([^\)]+)\)", text)
            if match_text is not None:
                result_node_list.append(TextNode(text[:match_text.start()], old_node.text_type))
                result_node_list.append(TextNode(match_text.group(1), TextType.IMAGE, match_text.group(2)))
                text = text[match_text.end():]
            else:
                result_node_list.append(TextNode(text, old_node.text_type))
                text = ""
    return result_node_list

def text_to_textnodes(text : str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

