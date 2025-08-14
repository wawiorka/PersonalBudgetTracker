# Personal Budget Tracker
## Учет доходов/расходов, категории, графики.
# Темы: 
- расчёты, 
- диаграммы, 
- фильтрация.

# ФУНКЦИОНАЛ:
- авторизация
- приватность
- CRUD доходов по категориям
- CRUD расходов по категориям
- баланс (отрицательным быть не может)
- графики

# Нюансы:
- Дефолтные категории доходов и расходов (incomes/expenses) заполняются через дата-миграции

## Структура проекта:
# Back-end
В рамках проекта tracker реализованы следующие приложения:

- [x] balances : баланс по 2 категориям: текущий и накопления
- [x] expenses : расходы по категориям
- [x] incomes : доходы по категориям
- [x] users : пользователи

# Front-end part (html, js, css)
- [x] Home : Стартовая страница
- [x] Expense Dashboard : Диаграмма расходов
- [x] Income Dashboard : Диаграмма доходов

## Установка и настойка:
Структура файла .env :

```env
DB_SECRET_KEY=
DB_DEBUG=
DB_ALLOWED_HOSTS=
DB_NAME=
DB_USER=
DB_USER_PASSWORD=
DB_HOST=
DB_PORT=
```
Из консоли :
```bash

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Изменения в settings.py:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    'balances',
    'expenses',
    'incomes',
    'users',
]
```

## Built With

* [Django 5.2.1](https://docs.djangoproject.com/en/5.2/releases/5.2.1/) - The web framework used
* [Django REST framework 3.16.0](https://www.django-rest-framework.org/) - The REST framework used
* [Psycopg 2.9.10](https://www.psycopg.org/docs/install.html) - Object-relational database system used
* [Simple JWT 5.5.0](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) - JSON Web Token authentication plugin
* [DFR spectacular 0.28.0](https://drf-spectacular.readthedocs.io/en/latest/#) - OpenAPI 3 schema generation
* [DFR spectacular sidecar 2025.6.1](https://drf-spectacular.readthedocs.io/en/latest/#) - self-contained OpenAPI 3 schema generation