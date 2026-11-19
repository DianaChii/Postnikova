import pytest
from services.renderer import MarkdownRenderer


class TestRenderer:
    def test_renders_basic_markdown(self):
        renderer = MarkdownRenderer()
        html, toc = renderer.render("# Заголовок\n\nТекст.")
        assert "<h1" in html
        assert "Заголовок" in html
        assert "Текст." in html

    def test_renders_tables(self):
        renderer = MarkdownRenderer()
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        html, _ = renderer.render(md)
        assert "<table>" in html
        assert "<th>A</th>" in html

    def test_renders_danger_admonition(self):
        renderer = MarkdownRenderer()
        md = '!!! danger "Опасно"\n    Текст опасности.'
        html, _ = renderer.render(md)
        assert "admonition" in html
        assert "danger" in html
        assert "Опасно" in html

    def test_renders_code_block(self):
        renderer = MarkdownRenderer()
        md = "```python\nprint('hello')\n```"
        html, _ = renderer.render(md)
        assert "codehilite" in html or "<code" in html

    def test_generates_toc(self):
        renderer = MarkdownRenderer()
        md = "# Первый\n\n## Подраздел\n\nТекст."
        html, toc = renderer.render(md)
        assert len(toc) > 0
        assert "Первый" in toc or "Подраздел" in toc
