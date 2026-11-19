import markdown
from typing import Tuple


class MarkdownRenderer:
    def __init__(self):
        self.extensions = [
            'toc', 'fenced_code', 'codehilite', 'tables', 'admonition'
        ]
        self.extension_configs = {
            'codehilite': {'css_class': 'codehilite', 'guess_lang': False},
            'toc': {'title': 'Содержание', 'toc_depth': '2-3'}
        }

    def render(self, text: str) -> Tuple[str, str]:
        md = markdown.Markdown(
            extensions=self.extensions,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        html = md.convert(text)
        toc = getattr(md, 'toc', '')
        return html, toc
