import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_init_without_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertEqual(node.url, None)

    def test_init_with_url(self):
        node = TextNode("This is a url node", TextType.LINK, "https://www.youtube.com/watch?v=xJXJXguW684")
        self.assertEqual(node.text, "This is a url node")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://www.youtube.com/watch?v=xJXJXguW684")

    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(str(node), "TextNode(This is a text node, text, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a url node", TextType.LINK, "https://www.youtube.com/watch?v=xJXJXguW684")
        self.assertEqual(str(node), "TextNode(This is a url node, link, https://www.youtube.com/watch?v=xJXJXguW684)")

if __name__ == "__main__":
    unittest.main()