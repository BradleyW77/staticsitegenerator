from textnode import TextType, TextNode

def main():
    text_node = TextNode("This is some test text.", TextType.LINK, "https://www.google.com")
    print(text_node)

main()
