# Проект Foodgram

## Описание

**Foodgram** - это проект, сайт, который позволяет регистрироваться пользователям и публиковать свои рецепты в общий доступ. Также сайт позволяет подписываться на пользователей, добавялть рецепты в избранное и создавать удобный список покупок, который можно скачать и использовать по своему усмотрению.

## Технологии

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-0000FF?style=for-the-badge&logo=docker&logoColor=white)

## Автор

### [Кирилл Мансуров](https://github.com/Kirill374mansurov)</br>  

## Функциональность

- Можно зарегистрироваться и создать свой профиль в котором можно менять аватарку
- Создать рецепт и опубликовать его на сайте
- Просматривать все доступные рецепты других пользователей
- Добавить понравившееся рецепты в избранные
- Подписаться на других пользователей
- Добавить ингредиенты блюд в список покупок

## Ресурсы API

- `/auth/`: Аутентификация
- `/users/`: Управление пользователями
- `/tags/`: Просмотр тегов
- `/ingredients/`: Просмотр ингредиентов
- `/recipes/`: Управление рецептами

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Kirill374mansurov/foodgram.git
```

Запустить проект в Docker:

```
docker compose up --build
```

## Примеры запросов к API:

### Регистрация нового пользователя:

Права доступа: **Доступно без токена**

```http request
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "^w\\Z"
}
```

### Получение JWT-токена:

Права доступа: **Доступно без токена**

```http request
POST http://127.0.0.1:8000/api/v1/auth/token/
Content-Type: application/json

{
"username": "^w\\Z",
"confirmation_code": "string"
}
```

### Получение списка всех категорий:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/categories/
```

### Добавление новой категории:

Права доступа: **Администратор**

```http request
POST http://127.0.0.1:8000/api/v1/categories/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "name": "string",
  "slug": "^-$"
}
```

### Удаление категории:

Права доступа: **Администратор**

```http request
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
Authorization: Bearer <your_access_token>
```

### Получение списка всех жанров:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/genres/
```

### Добавление жанра:

Права доступа: **Администратор**

```http request
POST http://127.0.0.1:8000/api/v1/genres/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "name": "string",
  "slug": "^-$"
}
```

### Удаление жанра:

Права доступа: **Администратор**

```http request
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
Authorization: Bearer <your_access_token>
```

### Получение списка всех произведений:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/titles/
```

### Добавление произведения:

Права доступа: **Администратор**

```http request
POST http://127.0.0.1:8000/api/v1/titles/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

### Частичное обновление информации о произведении:

Права доступа: **Администратор**

```http request
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

### Удаление произведения:

Права доступа: **Администратор**

```http request
DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Authorization: Bearer <your_access_token>
```

### Получение списка всех отзывов:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```


### Получение информации о произведении:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

### Добавление нового отзыва:

Права доступа: **Аутентифицированные пользователи**

```http request
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "text": "string",
  "score": 1
}
```

### Получение отзыва по id:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

### Частичное обновление отзыва по id:

Права доступа: **Автор отзыва, модератор или администратор**

```http request
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "text": "string",
  "score": 1
}
```

### Удаление отзыва по id:

Права доступа: **Автор отзыва, модератор или администратор**

```http request
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Authorization: Bearer <your_access_token>
```

### Получение списка всех комментариев к отзыву:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

### Добавление комментария к отзыву:

Права доступа: **Аутентифицированные пользователи**

```http request
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "text": "string"
}
```

### Получение комментария к отзыву:

Права доступа: **Доступно без токена**

```http request
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

### Частичное обновление комментария к отзыву:

Права доступа: **Автор комментария, модератор или администратор**

```http request
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "text": "string"
}
```

### Удаление комментария к отзыву:

Права доступа: **Автор комментария, модератор или администратор**

```http request
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Authorization: Bearer <your_access_token>
```

### Получение списка всех пользователей:

Права доступа: **Администратор**

```http request
GET http://127.0.0.1:8000/api/v1/users/
Authorization: Bearer <your_access_token>
```

### Добавление пользователя:

Права доступа: **Администратор**

```http request
POST http://127.0.0.1:8000/api/v1/users/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "username": "^w\\Z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Получение пользователя по username:

Права доступа: **Администратор**

```http request
GET http://127.0.0.1:8000/api/v1/users/{username}/
Authorization: Bearer <your_access_token>
```

### Изменение данных пользователя по username:

Права доступа: **Администратор**

```http request
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "username": "^w\\Z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Удаление пользователя по username:

Права доступа: **Администратор**

```http request
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
Authorization: Bearer <your_access_token>
```

### Получение данных своей учетной записи:

Права доступа: **Любой авторизованный пользователь**

```http request
GET http://127.0.0.1:8000/api/v1/users/me/
Authorization: Bearer <your_access_token>
```

### Изменение данных своей учетной записи:

Права доступа: **Любой авторизованный пользователь**

```http request
PATCH http://127.0.0.1:8000/api/v1/users/me/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
  "username": "^w\\Z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```