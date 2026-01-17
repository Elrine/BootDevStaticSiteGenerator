import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")

    def test_repr_fill(self):
        node = HTMLNode()
        node.tag = "ul"
        node.props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        child_node = HTMLNode()
        child_node.tag = "il"
        child_node.value = "Master"
        node.children = [child_node]
        self.assertEqual(str(node), "HTMLNode(ul, None, [HTMLNode(il, Master, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_props_to_html(self):
        node = HTMLNode()
        node.props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")


class TestLeafNode(unittest.TestCase):
    def test_init_without_props(self):
        node = LeafNode("p", "test")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_init_with_props(self):
        node = LeafNode("a", "link", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_to_html_without_value(self):
        with self.assertRaises(ValueError) as cm:
            LeafNode("p", None).to_html()
        exception_value = cm.exception
        self.assertEqual(exception_value.args, ("Value missing",))

    def test_to_html_without_tag(self):
        self.assertEqual(LeafNode(None, "test").to_html(), "test")

    def test_to_html_without_props(self):
        self.assertEqual(LeafNode("p", "test").to_html(), "<p>test</p>")

    def test_to_html_with_props(self):
        self.assertEqual(LeafNode("a", "link", {"href": "https://www.google.com"}).to_html(), "<a href=\"https://www.google.com\">link</a>")

    def test_repr(self):
        self.assertEqual(str(LeafNode("p", "test")), "LeafNode(p, test, None)")
    

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [child_node]).to_html()
        exception_value = cm.exception
        self.assertEqual(exception_value.args, ("Tag missing",))
        

    def test_to_html_without_child(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", None).to_html()
        exception_value = cm.exception
        self.assertEqual(exception_value.args, ("Children missing",))

    def test_repr_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(str(parent_node), "ParentNode(div, [LeafNode(span, child, None)], None)")

    def test_repr_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            str(parent_node),
            "ParentNode(div, [ParentNode(span, [LeafNode(b, grandchild, None)], None)], None)",
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_link(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://imgs.search.brave.com/YVV4ux7tv7fuEqP_WeVmXRe0ch7p9N83lTICdLpcUA0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9wcmV2/aWV3LnJlZGQuaXQv/c29tZS1vZi1teS1h/bGwtdGltZS1mYXZv/cml0ZS1hdmF0YXIt/ZmFuYXJ0LWJ5LXYw/LXFiMHc3OHJ0dWxr/ZTEuanBnP3dpZHRo/PTY0MCZjcm9wPXNt/YXJ0JmF1dG89d2Vi/cCZzPTM1OTVhYmY0/MTU4NTNkZTlmYWIx/MDYzOTg3MWJlNzg3/N2RiYjQwZTE")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://imgs.search.brave.com/YVV4ux7tv7fuEqP_WeVmXRe0ch7p9N83lTICdLpcUA0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9wcmV2/aWV3LnJlZGQuaXQv/c29tZS1vZi1teS1h/bGwtdGltZS1mYXZv/cml0ZS1hdmF0YXIt/ZmFuYXJ0LWJ5LXYw/LXFiMHc3OHJ0dWxr/ZTEuanBnP3dpZHRo/PTY0MCZjcm9wPXNt/YXJ0JmF1dG89d2Vi/cCZzPTM1OTVhYmY0/MTU4NTNkZTlmYWIx/MDYzOTg3MWJlNzg3/N2RiYjQwZTE", "alt": "This is a image node"})

if __name__ == "__main__":
    unittest.main()