[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org) 
# Тестовое задание. API. 

## Информация 
API для парсинга URL-адресов.

## Установка

Необходим Python версии 3.8.
Клонируйте репозиторий и введите в командной строке:

`git clone git@github.com:epsilonm/api_final_yatube.git`

`cd api_final_yatube`

Активируйте виртуальное окружение.

`python3 -m venv venv`

`source venv/Scripts/activate`

Обновите pip установите необходимые библиотеки из **requirements.txt**

`python3 -m pip install --upgrade pip`

`pip install -r requirements.txt`

Run API

`python3 api.py`

## Примеры использования

### Передача URL-адреса через GET-запрос с помощью параметров
Обрабатывает полученную с помощью GET-запроса URL-адрес.
Записывает в лог данные о протоколе, доменном имени, пути,
параметрах URL-адреса, а также домене системы управления репозиториями
и названии репозитория при их наличии.
#### Request

`GET /parse_link?https://github.com/CosmoFox/css`

`http://127.0.0.1:5000/parse_link?https://github.com/CosmoFox/css`

#### Response

```
HTTP status: 200
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
1. Статус 201. ID: 1
2. Статус 422. Ошибка валидации URL. Убедитесь, что все URL начинаются с http://.
```
