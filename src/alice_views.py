"""Модуль с функциями представления при работе с пользователем
навыков Алисы."""

from flask import Blueprint, make_response, request, session
from .analyzer import Analyzer


bp = Blueprint('alice', __name__, url_prefix='/alice')


@bp.route('/', methods=('POST',))
def main():
    """Функция представления обрабатывает запросы на странице с игрой."""

    data = request.get_json()
    response = {
        'response': {'text': ''},
        'version': data.get('version'),
        'session': data.get('session'),
        'session': {'end_session': False}
    }
    analyzer = Analyzer(session)
    analyzer.make_response(data, response)
    return make_response(response)
