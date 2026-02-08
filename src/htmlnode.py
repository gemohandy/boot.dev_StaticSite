class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This is not implemented.")
    
    def props_to_html(self):
        if(self.props == None):
            return ""
        out = ""
        for prop in self.props:
            out += f" {prop}=\"{self.props[prop]}\""
        return out
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node with no value!")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag on parent node?")
        if self.children == None:
            raise ValueError("No children on parent node?")
        out = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            try:
                out += child.to_html()
            except Exception as e:
                print(child)
                raise e
        out += f"</{self.tag}>"
        return out
