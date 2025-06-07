from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)
        self.children = None

    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"