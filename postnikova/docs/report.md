---
title: Отчёт по лабораторной работе
section: Отчёт
order: 1
tags: [отчёт]
---

# Отчёт по лабораторной работе

**Студент:** [Постникова В.О.]  
**Группа:** [455]  
**Вариант:** № 7 — Документация IoT-устройства  
**Репозиторий:** [https://github.com/DianaChii/Postnikova.git]  
**Дата:** 18.11.2026

## 1. Цель работы
Разработать веб-приложение DocHub для публикации технической документации IoT-контроллера SmartSense и на этом примере освоить паттерн MVC в Python/Flask.

## 2. Постановка задачи и предметная область
Документируется IoT-контроллер SmartSense. Целевая аудитория документации:
- **Разработчики** — API и архитектура системы.
- **Инженеры-схемотехники** — распиновка GPIO, параметры питания.
- **Монтажники** — техника безопасности при установке и подключении.

## 3. Обоснование выбора инструментов

| Инструмент | Роль в проекте | Почему выбран | Рассмотренные альтернативы |
|---|---|---|---|
| Flask | веб-каркас | MVC собирается вручную, каждый слой виден и контролируется | Django, FastAPI |
| Python-Markdown | рендеринг | Поддержка расширений: `toc`, `admonition`, `codehilite` | markdown-it-py, mistune |
| Pygments | подсветка кода | Серверная генерация CSS-классов для блоков кода | highlight.js (клиентская) |
| Файловая система | хранилище | Простота, подход docs-as-code, не требует БД | SQLite, Git |

## 4. Архитектура приложения

### 4.1 Разделение по MVC

| Компонент | Файлы | Что делает | От чего НЕ зависит |
|---|---|---|---|
| **Model** | `models/document.py`, `models/repository.py` | Сущность Document, разбор front matter, безопасный доступ к файлам | Flask, Jinja2, HTTP |
| **Service** | `services/renderer.py` | Преобразование Markdown → HTML, генерация TOC и подсветка | Flask, HTTP, шаблоны |
| **Controller** | `controllers/docs_controller.py`, `api_controller.py` | Приём HTTP-запросов, маршрутизация, вызов сервисов | HTML-строки, логика парсинга |
| **View** | `views/*.html`, `static/style.css` | Отображение данных, стилизация | Файловая система, БД |

### 4.2 Диаграмма пути запроса
```text
GET /docs/<slug>
  → docs_controller.show(slug)
    → DocumentRepository.get(slug)
      → Document.from_file() (чтение и парсинг YAML)
    → MarkdownRenderer.render(content)
    → render_template('document.html', doc=doc)
  → HTML 200 OK

4.3 Спорное решение
Рендерер Markdown помещён в слой services/, а не в views/ или controllers/, потому что это чистая доменная логика преобразования текста. Он не зависит от HTTP-запросов и шаблонизатора. Это позволяет переиспользовать его в будущем (например, для генерации PDF или JSON-экспорта) без изменения контроллеров.
5. Реализация
5.1 Ключевые фрагменты кода
Защита от path traversal (models/repository.py):

def _safe_path(self, slug: str) -> Optional[Path]:
    target = (self.docs_dir / slug).with_suffix('.md')
    try:
        target_resolved = target.resolve()
        # Проверяем, что путь находится строго внутри папки docs
        if not target_resolved.is_relative_to(self.docs_dir):
            return None
    except (ValueError, OSError):
        return None
    return target if target.exists() else None

Рендеринг Markdown (services/renderer.py):

def render(self, text: str) -> Tuple[str, str]:
    md = markdown.Markdown(
        extensions=['toc', 'fenced_code', 'codehilite', 'tables', 'admonition'],
        extension_configs={'codehilite': {'css_class': 'codehilite'}},
        output_format='html5'
    )
    html = md.convert(text)
    toc = getattr(md, 'toc', '')
    return html, toc

5.2 Трудности и как решены

|Проблема|Причина|Решение|
|Дублирование меню на главной странице|Передавал переменную sections и в base.html, и в index.html|Убрал цикл из index.html, оставил рендеринг меню только в base.html|
|Стандартная серая страница 404 от Flask|Не был зарегистрирован глобальный обработчик ошибок|Добавил @app.errorhandler(404) в app.py с возвратом render_template|
|Уязвимость Path traversal|Использование open(slug) без нормализации пути|Реализовал проверку через Path.resolve().is_relative_to()|

6. Тестирование

|Тест|Что проверяет|Слой|
|test_from_file_parses_front_matter|Корректный парсинг YAML-метаданных|Model|
|test_from_file_reads_content|Чтение тела документа|Model|
|test_list_returns_all_documents|Возврат списка всех документов|Model|
|test_list_sorted_by_section_and_order|Сортировка документов по разделам|Model|
|test_get_existing_document|Успешное получение документа по slug|Model|
|test_get_nonexistent_returns_none|Возврат None для несуществующего файла|Model|
|test_path_traversal_blocked|Блокировка попытки чтения ..passwd|Model|
|test_renders_basic_markdown|Базовое преобразование заголовков и текста|Service|
|test_renders_tables|Корректный HTML-вывод таблиц|Service|
|test_renders_danger_admonition|Генерация HTML-блока с классом admonition danger|Service|
|test_renders_code_block|Подсветка синтаксиса в блоках кода|Service|
test_generates_toc|Автоматическая генерация оглавления|Service|

Результат запуска: 12 passed in 0.07s

7. Комплект документации

|Файл|Тип Diátaxis|Аудитория|
|docs/index.md|explanation|Все|
|docs/guide/getting-started.md|tutorial|Новички|
|docs/guide/how-to-wifi.md|how-to|Пользователи|
|docs/guide/how-to-safety.md|how-to|Монтажники|
|docs/reference/pins.md|reference|Инженеры|
|docs/reference/api.md|reference|Разработчики|
|docs/reference/data-model.md|reference|Разработчики|
|docs/architecture/mvc.md|explanation|Разработчики|
|docs/architecture/adr-001.md|explanation|Разработчики|

8. Сравнение с MkDocs Material

|Возможность|MkDocs|Моя реализация|Вывод|
|Навигация из конфигурации|✔ из mkdocs.yml|✔ из front matter|У меня автоматически из файлов|
|Полнотекстовый поиск|✔ lunr.js|✔ по подстроке|У меня проще, без ранжирования|
|Оглавление страницы|✔|✔ через toc-расширение|Одинаково|
|Версионирование|✔ (mike)|✘|Не реализовано|
|Редактирование в браузере|✘|✘|Не реализовано|
|Темы оформления|✔ 20+ тем|1 тема|У меня проще, своя CSS|

9. Выполненные задания

|Код|Задание|Статус|
|M1|Модель + защита путей|✔|
|M2|Front matter + навигация|
|M3|Рендеринг Markdown|✔|
|M4|Все маршруты + 404|✔|
|M5|Шаблоны + адаптивность|✔|
|M6|Поиск + JSON API|✔|
|M7|Комплект документации (≥ 6 файлов, 4 типа)|✔|
|M8|≥ 8 тестов + path traversal|✔ (12 тестов)|
M9|Отчёт в системе|✔|

10. Выводы
Освоены: синтаксис Markdown и подход docs-as-code, строгое разделение слоёв MVC, тестирование модели изолированно от веб-фреймворка. В следующий раз добавил бы санитайзинг HTML через библиотеку bleach и версионирование документов через git log.
11. Источники

    Flask Documentation — https://flask.palletsprojects.com/
    Python-Markdown Extensions — https://python-markdown.github.io/extensions/
    Diátaxis Framework — https://diataxis.fr/
    Методическое руководство к лабораторной работе «DocHub».




