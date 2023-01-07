[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org) 
# Тестовое задание. API. 

## Информация 
API для парсинга URL-адресов.

## Установка

Необходим Python версии 3.8.
Клонируйте репозиторий и введите в командной строке:

`git clone git@github.com:epsilonm/test_api.git`

`cd test_api`

Активируйте виртуальное окружение.

`python -m venv venv`

`source venv/Scripts/activate`

Обновите pip установите необходимые библиотеки из **requirements.txt**

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

Run API

`flask --app api --debug run`

## Примеры использования

### Передача URL-адреса через POST-запрос с помощью параметров
Обрабатывает полученный в теле POST-запроса URL-адрес.
Записывает в лог данные о протоколе, доменном имени, пути,
параметрах URL-адреса, а также домене системы управления репозиториями
и названии репозитория при их наличии.
#### Request
Для обработки запроса нужно указать query-параметр link=link:

`POST /parse_link/<url>?link=link`

`http://127.0.0.1:5000/parse_link/https://github.com/CosmoFox/css?link=link`

#### Response

```
{
    "message": "Ваша ссылка принята"
}
```
Если query-параметр задан неверно или не указан::

#### Request
`POST /parse_link/https://github.com/CosmoFox/css?link=incorrect`

`http://127.0.0.1:5000/parse_link/https://github.com/CosmoFox/css?link=incorrect`

#### Response
```
{
    "message": "Указаны неверные query-параметры"
}
```

### Загрузка .csv файла через POST-запрос
Загружает .csv файл с URL-адресами посредством POST-запроса.
Возвращает перечень сообщений о статусе проверки URL-адресов:
Если адрес валиден:

```{номер строки}. {HTTP статус}. {ID адреса} ```

Если адрес не валиден:

```{номер строки}. {HTTP статус}. {сообщение об ошибке}.```

#### Request

`POST /upload`

`http://127.0.0.1:5000//upload`

##### File Payload
```
https://stackoverflow.com/questions/19898283/folder-and-files-upload-with-flask
http:www.example.com/main.html
```

#### Response

```
[
    {
        "id": 17,
        "line_number": 1,
        "status": 201
    },
    {
        "extra": "Ошибка валидации URL. Убедитесь, что все URL начинаются с http://.",
        "line_number": 2,
        "status": 422
    }
]
```
