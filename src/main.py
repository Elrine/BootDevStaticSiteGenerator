from textnode import TextNode, TextType

def main():
    first_el = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(first_el)

main()

