import os
from pathlib import Path
from typing import List, Optional
from .document import Document


class DocumentRepository:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir).resolve()
        if not self.docs_dir.exists():
            raise ValueError(f"Docs directory does not exist: {docs_dir}")

    def _safe_path(self, slug: str) -> Optional[Path]:
        """Защита от path traversal"""
        if not slug:
            slug = 'index'
        if slug.endswith('.md'):
            slug = slug[:-3]
        
        target = (self.docs_dir / slug).with_suffix('.md')
        
        try:
            target_resolved = target.resolve()
            if not target_resolved.is_relative_to(self.docs_dir):
                return None
        except (ValueError, OSError):
            return None
        
        return target if target.exists() else None

    def get(self, slug: str) -> Optional[Document]:
        path = self._safe_path(slug)
        if not path:
            return None
        return Document.from_file(str(path), slug)

    def list(self) -> List[Document]:
        documents = []
        for md_file in self.docs_dir.rglob('*.md'):
            rel_path = md_file.relative_to(self.docs_dir)
            slug = str(rel_path.with_suffix('')).replace(os.sep, '/')
            try:
                doc = Document.from_file(str(md_file), slug)
                documents.append(doc)
            except Exception as e:
                print(f"Error loading {md_file}: {e}")
                continue
        documents.sort(key=lambda d: (d.section, d.order))
        return documents
