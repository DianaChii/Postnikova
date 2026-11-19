---
title: Архитектура MVC
section: Архитектура
order: 1
tags: [explanation, architecture]
---

# Архитектура DocHub

## Разделение ответственности

| Слой | Файлы | Ответственность |
|------|-------|-----------------|
| Model | `models/document.py`, `models/repository.py` | Сущности, доступ к данным, бизнес-логика |
| Service | `services/renderer.py`, `services/search.py` | Доменные сервисы (рендеринг, поиск) |
| Controller | `controllers/docs_controller.py`, `controllers/api_controller.py` | Обработка HTTP-запросов, маршрутизация |
| View | `views/*.html`, `static/style.css` | Отображение, стили |

## Поток запроса
GET /docs/getting-started
    ↓
Controller (docs_controller.py)
    ↓
Model (DocumentRepository.get())
    ↓
Service (MarkdownRenderer.render())
    ↓
View (document.html)
    ↓
HTML ответ

## Почему рендерер в Service, а не в View?

Рендерер Markdown — это доменная логика преобразования текста. Он не зависит от HTTP или шаблонов. Если завтра мы захотим рендерить Markdown в PDF или JSON, нам не придётся менять контроллеры.

## Зависимости

- Controller → Model, Service, View
- Service → Model (иногда)
- Model → ничего (чистая бизнес-логика)
- View → ничего (только данные из контроллера)

!!! note "Принцип"
    Модель не знает о Flask. Её можно тестировать без веб-сервера.



