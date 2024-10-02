# Проект Foodgram

## Сайт проекта foodgramkirill.ddns.net

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