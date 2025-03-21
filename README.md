# 🛠️ RESTful API для приложения YaMDb

![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.12.4-green) ![Python](https://img.shields.io/badge/Python-3.9-blue) ![Django](https://img.shields.io/badge/Django-3.2-darkgreen)

# Описание проекта

REST API для сбора отзывов на произведения с возможностью регистрации с помощью `Email`
и аутентификации с использованием JWT-токенов.

## Реализованные технологии:

- 📧 **_Возможность регистрации через `Email` с кодом подтверждения_**
- 🔐 **_Аутентификация с помощью JWT-токенов_**
- 📄 **_CRUD-операции к эндпоинтам API_**
- 📝 **_Скрипты для заполнения базы данных из `CSV`-файлов_**

## Установка и запуск проекта локально:

1. **Склонируйте репозиторий в рабочее пространство:**

```bash
git clone https://github.com/forbxpg/api_yamdb
cd api_yamdb
```

2. **Разверните виртуальное окружение и установите зависимости:**

```
python -m venv env           [python3 -m venv env (Mac/Linux)]
source env/Scripts/activate  [env/bin/activate (Mac/Linux)]

pip install -r requirements.txt
```

3. **Примените миграции:**

```bash
python manage.py migrate
```

4. **Заполните базу данных тестовыми данными:**

```bash
python manage.py db_fill --all
```

5. **Запустите локальный сервер:**

```bash
python manage.py runserver
```


## 🔨Работа API

К проекту по адресу `/redoc/` подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

### 🖇️ Ресурсы API

- `auth`: аутентификация.
- `users`: пользователи.
- `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### 👥 Система для работы с пользователями

- **_Аноним:_** может просматривать описания произведений, читать отзывы и комментарии.
- **_Аутентифицированный пользователь `(user)`:_** может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **_Модератор `(moderator)`:_** те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **_Администратор `(admin)`:_** полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. Суперюзер Django должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Самостоятельная регистрация новых пользователей

Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`. Сервис YaMDB отправляет письмо с кодом подтверждения `(confirmation_code)` на указанный адрес `email`. Пользователь отправляет `POST`-запрос с параметрами username и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен). В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. После регистрации и получения токена пользователь может отправить `PATCH`-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором

Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно. После этого пользователь должен самостоятельно отправить свой `email` и `username` на эндпоинт `/api/v1/auth/signup/` , в ответ ему должно прийти письмо с кодом подтверждения. Далее пользователь отправляет `POST`-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

## Работа команд для заполнения базы данных из CSV-файлов
В директории `data` находятся файлы с данными для заполнения базы данных. Для заполнения базы данных данными из файлов используются команды:
```
python manage.py db_fill --<flag>:
 <flag>:
    --users       # заполнение таблицы пользователей
    --category    # заполнение таблицы категорий
    --genre       # заполнение таблицы жанров
    --title       # заполнение таблицы произведений
    --review      # заполнение таблицы отзывов
    --comments    # заполнение таблицы комментариев
    --genre_title # заполнение связанных таблиц жанров и произведений
    --all         # заполнение всех таблиц
```
⚠️ ***Предупреждение!***

При заполнении таблиц убедитесь, что если у модели есть поле, которое ссылается на другую модель, то вторая модель должна быть заполнена данными до заполнения первой модели!

Подробнее о командах можно узнать в документации их класса: `reviews/management/commands/db_fill.py - Command`

## 💻 Стек технологий

- **Python 3.9**
- **Django 3.2**
- **DjangoRestFramework 3.12**
- **DjangoRestFramework-SimpleJWT 4.7.2**

## ✍️ Контрибуторы:

- **[Линар Алеев](https://github.com/LinarAl)** - Работа с регистрацией и аутентификацией пользователей.
- **[Тимур Киргизов](https://github.com/forbxpg)** - Работа с произведениями, категориями, жанрами и заполнением БД.
- **[Алексей Порошин](https://github.com/Supersup66)** - Работа с отзывами, комментариями и рейтингом произведений.
