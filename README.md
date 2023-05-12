## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Пользователь может оставить один отзыв к каждому произведению, может оставлять комментарии к отзывам.

Документация к API находится по эндпоинту `/redoc`

## Запуск проекта
1. Клонировать репозиторий.

2. Создать виртуальное окружение
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```

3. Установить зависимости
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

4. Выполнить миграции
```bash
python manage.py migrate
```

Дополнительно можно заполнить БД тестовыми данными
```bash
python manage.py load_test_data
```

Запуск проекта
```bash
python manage.py runserver
```

---
## Описание API

### Сервис предполагает использование ролей для управления доступом:

* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
* **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Суперюзер Django** — обладет правами администратора (admin)

---
### Регистрация пользователей

```http
POST /api/v1/auth/signup 
```
```json
{
  "username": "Bob",
  "email": "example@email.com"
}
```

### Получение токена для аутентификации:
#### тип: JWT token (Bearer)

```http
POST /api/v1/auth/token 
```
```json
{
  "username": "Bob",
  "confirmation_code": "<код подтверждения>"
}
```
Ответ:
```json
{
  "token": "<JWT token>"
}
```
---
### Ресурс categories
Управление категориями произведения

#### Методы доступные администратору: 

#### Список категорий
```http
GET /api/v1/categories/ 
```
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
#### Добавление новой категории
```http
POST /api/v1/categories/ 
```
```json
{
"name": "string",
"slug": "string"
}
```
#### Удаление категории
```
DELETE /api/v1/categories/{slug}/
```
---
### Ресурс genres
Описывает жанры произведений

#### Методы доступные администратору: 
##### Список жанров
```http
GET /api/v1/genres/ 
```
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

#### Добавление нового жанра
```http
POST /api/v1/genres/ 
```
```json
{
"name": "string",
"slug": "string"
}
```
#### Удаление жанра
```
DELETE /api/v1/genres/{slug}/
```
---
### Ресурс titles
Управление произведениями

#### Методы доступные администратору: 

##### Список произведений
```http
GET /api/v1/titles/ 
```
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
#### Добавление нового произведения
```http
POST /api/v1/titles/ 
```
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
#### Информация о произведении
```http
GET /api/v1/titles/{titles_id}/
```
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
#### Изменение полей произведения 
```http
PATCH /api/v1/titles/{titles_id}/
```
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
#### Удаление произведения
```http
DELETE /api/v1/titles/{titles_id}/
```

---

### Ресурс users
Управление пользователями

#### Методы доступные администратору: 

#### Список пользователей
```http
GET /api/v1/users/ 
```
#### Создание нового пользователя
```http
POST /api/v1/users/ 
```
```json
{
"username": "Bob",
"email": "example@valid.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "<user|moderator|admin>" 
}
```
#### Информация о пользователе
```http
GET /api/v1/users/{username}/
```
#### Изменение полей пользователя
```http
PATCH /api/v1/users/{username}/
```
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
#### удаление пользователя
```
DELETE /api/v1/users/{username}/
```
#### Методы доступные аутентифицированному пользователю

#### Получения своего профиля
```http
GET /api/v1/users/me/
```
#### Изменение полей в профиле
```http
PATCH /api/v1/users/me/
```
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
---

### Ресурс Reviews
Управление отзывами к произведениям

#### Примеры запросов и ответов сервера

#### Получение списка всех отзывов:
```http
GET /titles/123/reviews/
```
Ответ:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "Отличное произведение! Настоятельно рекомендую.",
            "author": "user1",
            "score": 10,
            "pub_date": "2022-04-28T12:30:00Z"
        },
        {
            "id": 2,
            "text": "Не очень понравилось.",
            "author": "user2",
            "score": 5,
            "pub_date": "2022-05-02T14:00:00Z"
        }
    ]
}
```

#### Добавление нового отзыва:
```http
GET /titles/123/reviews/456/
```
Ответ:
```json
{ 
  "id": 456,
  "text": "Отличное произведение, очень понравилось!",
  "author": "John Doe",
  "score": 5,
  "pub_date": "2023-05-10T10:30:00Z"
}
```
---

### Ресурс Comments
Управление комментариями к отзывам

#### Примеры запросов и ответов сервера
#### Изменение комментария:
```http
PATCH /api/v1/titles/123/reviews/456/comments/789/
Authorization: Bearer <jwt-token>
Content-Type: application/json
```
```json
{
  "text": "Новый текст комментария"
}
```
Ответ:
```http
HTTP/1.1 200 OK
Content-Type: application/json
```
```json
{
  "id": 789,
  "text": "Новый текст комментария",
  "author": "user123",
  "pub_date": "2023-05-11T10:00:00Z"
}
```

#### Добавление комментария:
```http
POST /api/v1/titles/123/reviews/456/comments/
Authorization: Bearer <jwt-token>
```
```json
{
"text": "Очень интересный комментарий!"
}
```
Ответ:
```json
{
"id": 789,
"text": "Очень интересный комментарий!",
"author": "user123",
"pub_date": "2023-05-11T10:30:00Z"
}
```
