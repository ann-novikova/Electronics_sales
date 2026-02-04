# Электронная Торговая Сеть (DistributorHub)

Веб-приложение для управления сетью по продаже электроники с API-интерфейсом и админ-панелью.

## Стек технологий

- Python 3.13+
- Django 6.0+
- Django REST Framework 3.16+
- PostgreSQL 17+

## Установка и запуск

### 1. Клонирование репозитория

#bash
git clone <https://github.com/ann-novikova/Electronics_sales.git>
#

### 2. Создание виртуального окружения

#bash
python -m venv venv
#

### 3. Активация виртуального окружения

**Linux/MacOS:**
#bash
source venv/bin/activate
#

**Windows:**
#bash
venv\Scripts\activate
#

### 4. Установка зависимостей

#bash
pip install -r requirements.txt
#

### 5. Настройка базы данных

Создайте файл `.env` в корне проекта на основе .env_sample.

### 6. Применение миграций

#bash
python manage.py migrate
#

### 7. Создание суперпользователя

#bash
python manage.py createsuperuser
#

### 8. Запуск сервера

#bash
python manage.py runserver
#

Приложение будет доступно по адресу: http://localhost:8000

## API Endpoints

### Аутентификация
- `POST /api/auth/login/` - Вход
- `POST /api/auth/logout/` - Выход

### Звенья сети
- `GET /suppliers/` - Список всех звеньев
- `POST /suppliers/` - Создание нового звена
- `GET /suppliers/{id}/` - Детальная информация
- `PUT /suppliers/{id}/` - Полное обновление
- `PATCH /suppliers/{id}/` - Частичное обновление
- `DELETE /suppliers/{id}/` - Удаление

### Продукты
- `GET /products/` - Список всех продуктов
- `POST /products/` - Создание нового продукта
- `GET /products/{id}/` - Детальная информация
- `PUT /products/{id}/` - Полное обновление
- `PATCH /products/{id}/` - Частичное обновление
- `DELETE /products/{id}/` - Удаление

## Фильтрация и поиск

### Для звеньев сети:
- `GET /suppliers/?country=Россия`
- `GET /suppliers/?city=Санкт-Петербург`
- `GET /suppliers/?level=1`
- `GET /suppliers/?search=Завод`
- `GET /suppliers/?ordering=name`

### Для продуктов:
- `GET /products/?chain_node__country=Россия`
- `GET /products/?chain_node__city=Санкт-Петербург`
- `GET /products/?search=iPhone`
- `GET /products/?ordering=release_date`

## Админ-панель

Админ-панель доступна по адресу: `/admin/`

Особенности:
- Ссылка на поставщика на странице объекта
- Фильтр по городу в списке объектов
- Admin action для очистки задолженности
- Отображение иерархии сети

## Тестирование

Запуск тестов:

#bash
python manage.py test
#

Запуск с подробным выводом:

#bash
python manage.py test -v 2
#

## Модели данных

### DistributorNode (Звено сети)
- **Уровни**: 0-Завод, 1-Розничная сеть, 2-ИП
- **Контакты**: email, страна, город, улица, номер дома
- **Финансы**: задолженность перед поставщиком
- **Иерархия**: ссылка на поставщика

### Product (Продукт)
- Название, модель, дата выхода на рынок
- Связь с звеном сети

## Бизнес-правила

1. **Иерархия**: Завод → Розничная сеть → ИП
2. **Поставщики**: Завод не может иметь поставщика
3. **Задолженность**: Запрещено обновление через API
4. **Доступ**: Только активные сотрудники имеют доступ к API

## Разработчик:

*   **Git:** ann-novikova
*   **Проект:** Electronics_sales