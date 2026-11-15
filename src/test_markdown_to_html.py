import unittest
from markdown_to_html import markdown_to_html

class TestMarkdownToHTML(unittest.TestCase):
    def test_if_works(self) -> None:
        markdown = """
# This is a heading

## This is also a heading

```
This is a code block
```

- This is a list
- with _italicized items_

>This is quote text

1. This
2. is
3. an
4. ordered
5. list

a. This
b. is
c. also
d. an
e. ordered
f. list


``
failed code
```

--failed list

    - Tabbed UNORDERED_LIST
"""
        mth = markdown_to_html(markdown)

        #self.assertEqual(
        #    mth.to_html(),
        #    '<div><ul><li>This is a list</li><li>with <i>italicized items</i></li></ul>'
        #        + '<p>failed code```</p><p>--failed list</p><ul><li>Tabbed UNORDERED_LIST</li></ul></div>'
        #)

