import os
import pytest
from models.document import Document
from models.repository import DocumentRepository


@pytest.fixture
def docs_dir(tmp_path):
    """Создаёт временную папку с тестовыми документами"""
    doc1 = tmp_path / "index.md"
    doc1.write_text("""---
title: Тестовый документ
section: Тесты
order: 1
tags: [test]
---

# Заголовок

Текст документа.

!!! danger "Опасно"
    Это предупреждение.
""")
    
    doc2 = tmp_path / "guide.md"
    doc2.write_text("""---
title: Руководство
section: Тесты
order: 2
---

# Руководство

Ещё текст.
""")
    
    return tmp_path


class TestDocument:
    def test_from_file_parses_front_matter(self, docs_dir):
        doc = Document.from_file(str(docs_dir / "index.md"), "index")
        assert doc.title == "Тестовый документ"
        assert doc.section == "Тесты"
        assert doc.order == 1
        assert "test" in doc.tags

    def test_from_file_reads_content(self, docs_dir):
        doc = Document.from_file(str(docs_dir / "index.md"), "index")
        assert "Заголовок" in doc.content
        assert "!!! danger" in doc.content

    def test_from_file_defaults(self, docs_dir):
        doc = Document.from_file(str(docs_dir / "guide.md"), "guide")
        assert doc.tags == []


class TestRepository:
    def test_list_returns_all_documents(self, docs_dir):
        repo = DocumentRepository(str(docs_dir))
        docs = repo.list()
        assert len(docs) == 2

    def test_list_sorted_by_section_and_order(self, docs_dir):
        repo = DocumentRepository(str(docs_dir))
        docs = repo.list()
        assert docs[0].title == "Тестовый документ"
        assert docs[1].title == "Руководство"

    def test_get_existing_document(self, docs_dir):
        repo = DocumentRepository(str(docs_dir))
        doc = repo.get("index")
        assert doc is not None
        assert doc.title == "Тестовый документ"

    def test_get_nonexistent_returns_none(self, docs_dir):
        repo = DocumentRepository(str(docs_dir))
        doc = repo.get("nonexistent")
        assert doc is None

    def test_path_traversal_blocked(self, docs_dir):
        """Обязательный тест по методичке: защита от ../"""
        repo = DocumentRepository(str(docs_dir))
        doc = repo.get("../../etc/passwd")
        assert doc is None

    def test_path_traversal_with_encoded_dots(self, docs_dir):
        repo = DocumentRepository(str(docs_dir))
        doc = repo.get("../../../etc/passwd")
        assert doc is None
