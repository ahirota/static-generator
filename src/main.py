from textnode import TextNode, TextType

def main():
    sample_node = TextNode("Learn Backend Development", TextType.LINK, "https://www.boot.dev")
    print(sample_node)

if __name__ == "__main__":
    main()