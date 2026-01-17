from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown : str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block]

def block_to_block_type(block : str) -> BlockType:
    if re.fullmatch("#{1:6} .+", block):
        return BlockType.HEADING
    elif re.fullmatch("`{3}\n.+`{3}", block):
        return BlockType.CODE
    elif re.fullmatch("> [^\n]+(?:\n> [^\n]+)*", block):
        return BlockType.QUOTE
    elif re.fullmatch("- [^\n]+(?:\n- [^\n]+)*", block):
        return BlockType.UNORDERED_LIST
    elif re.fullmatch("(\d+)\. [^\n]+(?:\n(\d+)\. [^\n]+)*", block):
        match_order_list = re.findall("^(\d+)\. [^\n]+", block, flags=re.MULTILINE)
        for index in range(1, len(match_order_list) + 1):
            if index != match_order_list[index - 1]:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH