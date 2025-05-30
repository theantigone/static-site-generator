class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''

        items = []
        for key, value in self.props.items():
            items.append(f'{key}="{value}"')

        return ' '+' '.join(items)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
                self.tag == other.tag and
                self.value == other.value and
                self.props == other.props and
                self.children is None and other.children is None
        )

    def to_html(self):
        if self.value is None:
            raise ValueError('LeafNode requires a value.')
        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag and
            self.children == other.children and
            self.props == other.props and
            self.value is None and other.value is None
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError('ParentNode requires a tag.')
        if not self.children:
            raise ValueError('ParentNode requires a child.')

        return f'<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>'

    def __repr__(self):
        return f'ParentNode({self.tag}, {self.children}, {self.props})'
