[![Build Status](https://travis-ci.com/ko3luhbka/flask_microblog.svg?branch=master)](https://travis-ci.com/ko3luhbka/flask_microblog)
[![Coverage Status](https://coveralls.io/repos/github/ko3luhbka/flask_microblog/badge.svg)](https://coveralls.io/github/ko3luhbka/flask_microblog)

# Flaskr microblog app

Based on [official Flask project tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/) with improvements like unit tests, MySQL database instead of SQLite and ORM (SQLAlchemy).
Also uses Flask-migrate for database migrations.
Deployed with Docker & Docker Compose.

---

## How to run app

Prerequisites: Docker and Docker Compose shuld be installed.

1. `git clone`.
2. `cd flask_microblog`.
3. Set the following environment variables (using *nix `export` command or in .env file):
- `SECRET_KEY` - any long enough password-like string;
- `DATABASE_URL=mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@db:3306/{MYSQL_DATABASE}`;
- `MYSQL_DATABASE` - database name;
- `MYSQL_USER` - user for working with database;
- `MYSQL_PASSWORD` - user's password.
    NB! Substitute `{}` in `DATABASE_URL` variable with the appropriate values.
4. run command `docker-compose up`.
After the containers are fully started, the web interface is available on `localhost:8000`.

## How to stop app

run command `docker-compose down`.

## API endpoints

### Get blog user
##### URL
`/api/users/:id`
##### Method
`GET`
##### URL params
`id=[integer]`
##### Data params
`None`
##### Success response
  Code: 200 OK
  Content:
```json
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "post_count": 1,
        "username": "johndoe"
    }
```
##### Error response
  Code: 404 Not Found
  Content: `None`

### Get all blog users
##### URL
`/api/users`
##### Method
`GET`
##### URL params
`None`
##### Data params
`None`
##### Success response
  Code: 200
  Content:
```json
    {
        "count": 1,
        "users": [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "post_count": 1,
                "username": "johndoe"
            }
        ]
    }
```
##### Error response
  `None`

### Create new blog user
##### URL
`/api/users`
##### Method
`POST`
##### URL params
`None`
##### Data params
JSON:
```json
   {
    "first_name": "Jane",
    "last_name": "Smith",
    "password": supersecret,
    "username": "janesmith"
    }
```
##### Success response
  Code: 201
  Content:
```json
    {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith",
        "post_count": 0,
        "username": "janesmith"
    }
```
##### Error response
  Code: 400 Bad request
  Content: 
```json
  {
    "error": "Bad Request",
    "message": "The user is already exist, please use a different username"
  }
```

### Modify existing blog user
##### URL
`/api/users/:id`
##### Method
`PUT`
##### URL params
`id=[integer]`
##### Data params
JSON:
```json
   {
    "first_name": "Lorem",
    "last_name": "Ipsum",
    "username": "loremipsum"
    }
```
##### Success response
  Code: 200
  Content:
```json
    {
        "id": 2,
        "first_name": "Lorem",
        "last_name": "Ipsum",
        "username": "loremipsum",
        "post_count": 0,
    }
```
##### Error response
  Code: 404 Not Found
  Content: `None`
  Code: 400 Bad request
  Content: 
```json
  {
    "error": "Bad Request",
    "message": "Please use a different username"
  }
```

### Get blog post
##### URL
`/api/posts/:id`
##### Method
`GET`
##### URL params
`id=[integer]`
##### Data params
`None`
##### Success response
  Code: 200 OK
  Content:
```json
    {
    "author": {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe"
    },
    "author_id": 1,
    "body": "Hello world!",
    "created": "2020-03-23 11:46:10",
    "id": 1,
    "title": "hello"
}
```
##### Error response
  Code: 404 Not Found
  Content: `None`

### Get all users blog posts
##### URL
`/api/posts`
##### Method
`GET`
##### URL params
`None`
##### Data params
`None`
##### Success response
  Code: 200
  Content:
```json
    {
        "count": 1,
        "posts": [
            {
            "author": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe"
            },
            "author_id": 1,
            "body": "Hello world!",
            "created": "2020-03-23 11:46:10",
            "id": 1,
            "title": "hello"
            }
        ]
    }
```
##### Error response
  `None`

TODO: add delete & edit endpoints