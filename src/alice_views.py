"""Модуль с функциями представления, которые обрабатывают запросы пользователя
от Алисы."""

from flask import Blueprint, make_response, redirect, request, url_for
from .analyzer import Analyzer


bp = Blueprint('alice', __name__, url_prefix='/alice')


@bp.route('/', methods=('POST', 'GET'))
def main():
    """Функция представления обрабатывает запросы от Алисы."""

    if request.method == 'GET':
        # Если запрос с методом GET, то перенаправляем на главную страницу
        return redirect(url_for('site.index'))
    # Создаем обработчик запроса
    analyzer = Analyzer()
    # Обработка запроса POST: получаем идентификатор пользователя и город
    # от него
    try:
        data = request.get_json()
        user = data['session']['application']['application_id']
        text = data['request']['original_utterance'].strip().upper()
        new = data['session']['new']
    except:
        return make_response(analyzer.get_default())
    # Анализируется запрос и готовится ответ
    response = analyzer.make_response_to_alice(user, text, new)
    return make_response(response)
