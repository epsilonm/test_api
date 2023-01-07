import os
import re
from logging.config import dictConfig
from urllib.parse import urlparse, parse_qs

import validators
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

import csv


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'flask.log',
        'encoding': 'utf-8',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

UPLOAD_FOLDER = './csv/'
ALLOWED_EXTENSIONS = {'csv'}

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)
with app.app_context():
    db.create_all()


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=True)


@app.errorhandler(PermissionError)
def handle_permission_denied(e):
    return 'Неверное расширение файла: требуется .csv', 415


def allowed_file(filename):
    """Возвращает True, если расширение загруженного файла допустимое."""
    return '.' in filename and (
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def url_not_valid_reason(url):
    """Возвращает список ошибок, если ссылка невалидна."""
    errors = list()
    errors.append('Ошибка валидации URL.')
    if not re.findall(r'^https?://', url):
        errors.append('Убедитесь, что все URL начинаются с http://.')
    elif not re.findall(r'\\', url):
        errors.append(
            'Убедитесь, Вы не используете символ с обратной косой чертой "\\".'
        )
    return errors


def parse_csv(filename):
    """
    Проверяет URL адреса в .csv файле на валидность.
    Возвращает перечень сообщений о статусе проверки URL-адресов
    в формате json.
    """
    data = list()
    with open(app.config['UPLOAD_FOLDER'] + filename, "r") as file:
        csv_file = csv.reader(file)
        count = 0
        for row in csv_file:
            link = ''.join(row)
            count += 1
            if validators.url(link):
                if db.session.query(Link).filter_by(url=link).first():
                    data.append({
                        'line_number': count,
                        'status': 'ссылка уже существует',
                    })
                else:
                    valid_link = Link(url=link)
                    db.session.add(valid_link)
                    db.session.commit()
                    data.append({
                        'line_number': count,
                        'status': 201,
                        'id': valid_link.id
                    })
            else:
                message = " ".join(url_not_valid_reason(link))
                data.append({
                    'line_number': count,
                    'status': 422,
                    'extra': message
                })
    return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Загружает .csv файл с URL-адресами посредством POST-запроса.
    Передает имя файла как параметр функции parse_csv(filename).
    Возвращает результат выполнения parse_csv(filename).
    """
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(
            os.path.join(app.config['UPLOAD_FOLDER'], filename)
        )
    return parse_csv(filename)


@app.route('/parse_link', methods=['POST'])
def parse_link():
    """
    Обрабатывает полученную с помощью POST-запроса URL-адрес.
    Записывает в лог данные о протоколе, доменном имени, пути,
    параметрах URL-адреса, а также домене системы управления репозиториями
    и названии репозитория при их наличии.
    """
    user_message = {
            "message": "Ваша ссылка принята"
        }
    query = parse_qs(urlparse(request.url).query)
    params = "| ".join([f'{key} : {val} ' for key, val in query.items()])
    if not request.args.get('link'):
        user_message['message'] = (
            'Указаны неверные параметры запроса.'
            ' Пожалуйста, начните запрос с ?link=<url>'
            )
        app.logger.info(f'Неверные параметры запроса: {params}')
    else:
        body = urlparse(request.args.get('link'))._asdict()
        message = (
            f"Протокол: {body['scheme']} | Домен: {body[ 'netloc']} | "
            f"Путь: {body['path']} | Параметры: {params}"
        )
        if body['netloc'] == 'github.com' or body['netloc'] == 'gitlab.com':
            body['git'] = body['netloc']
            body['repo'] = body['path'].split('/')[-1].split('.')[0]
            message += f" | Гит: {body['git']} | Репозиторий: {body['repo']}"
        else:
            message += '- Ссылка не на гит'
        app.logger.info(message)

    return jsonify(user_message)


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':

    app.run(debug=True)
