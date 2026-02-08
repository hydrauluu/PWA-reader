# Техническое задание: Веб-библиотека для чтения книг

## 1. Общее описание
Веб-приложение для поиска, скачивания и чтения книг с интеграцией Flibusta через Tor.

## 2. Технологический стек
- Backend: Django
- Frontend: HTMX, Alpine.js, Tailwind CSS
- Язык интерфейса: русский
- Архитектура: SPA-подобный интерфейс

## 3. Структура проекта

```
library_project/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── books/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── services/
│   │   ├── flibusta_service.py
│   │   ├── fb2_parser.py
│   │   └── reading_service.py
│   └── templates/
│       └── books/
├── static/
│   ├── css/
│   ├── js/
└── media/
    ├── covers/
    └── books/
```

## 4. Модели данных

### 4.1 Book
```python
id: AutoField (PK)
title: CharField(max_length=500)
author: CharField(max_length=300)
cover: ImageField(upload_to='covers/')
file: FileField(upload_to='books/')
file_size: BigIntegerField()
format: CharField(max_length=10, default='fb2')
flibusta_id: CharField(max_length=100, unique=True, null=True)
added_date: DateTimeField(auto_now_add=True)
language: CharField(max_length=50, default='ru')
description: TextField(blank=True)
```

FONT_SIZES:
    - small: '14px'
    - medium: '16px'
    - large: '18px'
    - extra_large: '20px'

THEMES:
    - light: Светлая тема
    - dark: Тёмная тема
    - sepia: Сепия
```

## 5. API Endpoints

### 5.1 Библиотека
- `GET /` - главная страница со всеми книгами
- `GET /books/` - список книг (HTMX partial)
- `GET /books/<int:id>/` - карточка книги

### 5.2 Чтение
- `GET /books/<int:id>/read/` - страница чтения
- `GET /books/<int:id>/content/` - получение контента книги
- `POST /books/<int:id>/progress/` - сохранение прогресса
  - Body: `{ "progress_percent": 45.5, "last_position": 1234 }`

### 5.3 Поиск и скачивание
- `GET /search/` - поиск книг на Flibusta
  - Query: `?q=название книги`
- `POST /books/download/` - скачивание книги с Flibusta
  - Body: `{ "flibusta_id": "12345", "title": "...", "author": "..." }`

### 5.4 Настройки
- `GET /settings/` - получение настроек чтения
- `POST /settings/` - обновление настроек
  - Body: `{ "font_size": "large", "theme": "dark" }`

## 6. Пользовательские настройки чтения

### 6.1 Размеры шрифта
- Маленький: 14px
- Средний: 16px (по умолчанию)
- Большой: 18px
- Очень большой: 20px

### 6.2 Цветовые темы
- Светлая:
  - background: #FFFFFF
  - text: #1F2937
- Тёмная:
  - background: #1F2937
  - text: #F9FAFB
- Сепия:
  - background: #F4E8D8
  - text: #5C4B37
  
```

## 7. Зависимости (requirements.txt)

```
Django>=6.0
django-htmx>=1.17.0
Pillow
requests[socks]
PySocks
lxml
```

## 8. Функциональные требования

### 8.1 Главная страница (Библиотека)
- Отображение всех книг в виде сетки карточек
- Карточка книги содержит:
  - Обложку
  - Название
  - Автора
- Поле поиска в верхней части страницы
- Поиск книг через Flibusta .onion
- Скачивание найденных книг в формате .fb2 на сервер
- Автоматическое добавление скачанных книг в библиотеку

### 8.2 Страница чтения книги
- Отображение текста книги
- Сохранение прогресса чтения в процентах
- Меню настроек (открывается по клику в центр экрана):
  - Отображение текущего прогресса чтения
  - Настройка размера шрифта
  - Выбор цветовой темы

### 8.3 Интеграция с Flibusta
- Поиск книг через .onion домен Flibusta
- Парсинг результатов поиска
- Скачивание книг в формате .fb2
- Сохранение книг на сервере

## 9. Нефункциональные требования

### 9.1 Код
- Безопасность (защита от инъекций, XSS, CSRF)
- Принцип DRY (Don't Repeat Yourself)
- ООП подход
- Использование маппинга при необходимости
- Код без комментариев

### 9.2 Производительность
- SPA-подобная навигация без перезагрузки страницы
- Асинхронная загрузка контента через HTMX

### 9.3 Безопасность
- Проксирование запросов к Flibusta через Tor
- Валидация входных данных
- Защита от CSRF атак
- Безопасное хранение файлов

## 10. UI/UX требования
- Адаптивный дизайн
- Интуитивная навигация
- Плавные переходы между состояниями
- Индикаторы загрузки
- Feedback для пользовательских действий
