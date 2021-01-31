"""В модуле создается Flask-приложение."""

import os
from flask import Flask
from . import alice_views
from . import views


# Словарь для хранения данных сессий
session_data = {}

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'cities.sqlite'),
)

test_config = None
if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Простая функция представления для тестирования
@app.route('/hello/<string:name>', methods=('GET',))
def hello(name):
    return f'Hello, {name.upper()}!'


# Регистрируем функции представления
app.register_blueprint(alice_views.bp)
app.register_blueprint(views.bp)
