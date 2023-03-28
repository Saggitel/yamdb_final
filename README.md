![Workflow status.](https://github.com/Saggitel/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Проект YaMDb
### Описание
Проект **YaMDb** собирает отзывы пользователей на различные произведения, делящиеся на различные категории и жанры. Пользователи могут оставлять отзывы к произведениям, давать им оценку, а также обсуждать их в комментариях.

### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2. **YaMDB** отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле.

### Технологии
- Python 3.7
- Django 2.2.16
- Django REST Framework 3.12.4

### Установка
- Cоздать и активировать виртуальное окружение

```
python -m venv venv
```

```
source venv/scripts/activate
```

```
python -m pip install --upgrade pip
```
- Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Выполнить миграции

```
python manage.py migrate
```

- Запустить проект

```
python manage.py runserver
```

### Документация
Документация, содержащая примеры запросов, доступна по адресу: http://127.0.0.1:8000/redoc.

### Авторы
Тимур
