"""Модуль с функциями представления при работе с пользователем
навыков Алисы."""

from flask import (Blueprint, flash, make_response, redirect, render_template,
                   request, session, url_for)
from .analyzer import Analyzer


bp = Blueprint('alice', __name__, url_prefix='/alice')


@bp.route('/', methods=('POST',))
def main():
    """Функция представления обрабатывает запросы на странице с игрой."""

    data = request.get_json()
    response = {
        'version': data.get('version'),
        'session': data.get('session'),
        'session': {'end_session': False}
    }
    analyzer = Analyzer()
    analyzer.make_response(data, response)
    return json.dumps(response, ensure_ascii=False, indent=2)
