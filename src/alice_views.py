"""Модуль с функциями представления, которые обрабатывают запросы пользователя
от Алисы."""

from flask import Blueprint, make_response, redirect, request, session, url_for
from .analyzer import Analyzer


bp = Blueprint('alice', __name__, url_prefix='/alice')


@bp.route('/', methods=('POST', 'GET'))
def main():
    """Функция представления обрабатывает запросы от Алисы."""

    if request.method == 'GET':
        # Если запрос с методом GET, то перенаправляем на главную страницу
        return redirect(url_for('site.index'))
    # Обработка запроса POST
    data = request.get_json()
    if not data:
        # Если нет json-данных, то прекращаем обработку запроса
        return make_response({'info': 'Неверный формат запроса'})
    # Словарь для ответа Алисе
    response = {
        'response': {'text': ''},
        'version': data.get('version'),
        'session': data.get('session'),
        'session': {'end_session': False}
    }
    # Получаем идентификатор пользователя и город от него
    try:
        user = data['session']['user_id']
        user_city = data['request']['original_utterance'].strip().upper()
        new = data['session']['new']
    except:
        return make_response({'info': 'Неверный формат запроса'})
    analyzer = Analyzer(session, user)
    analyzer.make_response_to_alice(user_city, new, response)
    return make_response(response)
