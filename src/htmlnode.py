class HTMLNode:
    def __init__(self,
                 tag: str | None = None,
                 value: str | None = None,
                 children: list[HTMLNode] | None = None,
                 props: dict[str, str] | None = None
                 ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        rv = ''
        if self.props is not None:
            for prop in self.props:
                rv += f' {prop}="{self.props[prop]}"'
        return rv

    def __repr__(self):
        return f'HTMLNode("{self.tag}", "{self.value}", {self.children}, {str(self.props)})'

class LeafNode(HTMLNode):
    def __init__(self,
                 value: str,
                 tag: str | None = None,
                 props: dict[str, str] | None = None,
                 ) -> None:
        if value is None:
            raise ValueError('ERROR: No value given to LeafNode')
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            return f'{self.value}'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode("{self.tag}", "{self.value}", {str(self.props)})'

class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 children: list[HTMLNode],
                 props: dict[str, str] | None = None,
                 ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError('ERROR: No tag for ParentNode!')
        if self.children is None:
            raise ValueError('ERROR: No children for ParentNode!')
        join_hold = "".join(str(node.to_html()) for node in self.children)
        return f'<{self.tag}{self.props_to_html()}>{ join_hold }</{self.tag}>'

    def __repr__(self):
        return f'ParentNode(\n "{self.tag}",\n [\n  {"  ".join(str(child.__repr__() + ',\n') for child in self.children)} ],\n {str(self.props)}\n)'
