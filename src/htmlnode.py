from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag : str = tag
        self.value : str = value
        self.children : list[HTMLNode] = children
        self.props : dict = props

    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        html_value = ""
        if self.props is not None:
            for key, value in self.props.items():
                html_value += f" {key}=\"{value}\""
        return html_value
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag : str, value : str, props : dict = None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value missing")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag : str, children : list[HTMLNode], props : dict = None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Tag missing")
        if self.children is None:
            raise ValueError("Children missing")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
def text_node_to_html_node(text_node : TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {'src': text_node.url, 'alt': text_node.text})
    raise ValueError("Text node must have a valid type")