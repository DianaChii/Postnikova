from dataclasses import dataclass
from typing import Optional, List
import frontmatter


@dataclass
class Document:
    slug: str
    title: str
    content: str
    section: str = "Общее"
    order: int = 999
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    @classmethod
    def from_file(cls, file_path: str, slug: str) -> 'Document':
        post = frontmatter.load(file_path)
        return cls(
            slug=slug,
            title=post.get('title', slug),
            content=post.content,
            section=post.get('section', 'Общее'),
            order=post.get('order', 999),
            tags=post.get('tags', [])
        )
