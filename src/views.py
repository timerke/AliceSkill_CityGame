"""Модуль с функциями представления, которые обрабатывают запросы пользователя
на сайте."""

from flask import (Blueprint, escape, make_response, redirect, render_template,
                   request, session, url_for)
from .searcher import Searcher
from .analyzer import Analyzer


bp = Blueprint('site', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    """Функция представления обрабатывает запросы на исходной странице."""

    if request.method == 'POST':
        return redirect(url_for('site.game'))
    return render_template('index.html')


@bp.route('/finish', methods=('POST',))
def finish():
    """Функция представления обрабатывает запрос на завершение игры."""

    from .main import session_data
    user = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    session.clear()
    session_data.pop(user, None)
    return redirect(url_for('site.index'))


@bp.route('/game', methods=('GET', 'POST'))
def game():
    """Функция представления обрабатывает запросы-ответы в игре."""

    if request.method == 'GET':
        # Получаем ip адрес пользователя и сохраняем его
        from .main import session_data
        user = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        session.clear()
        session['user'] = user
        # Очищаем историю игры
        session_data[user] = []
        # Очищаем куки
        response = make_response(render_template('game.html'))
        response.set_cookie('letter', '', max_age=0)
        return response
    # Обработка запроса POST
    user = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if session.get('user') != user:
        return render_template('index.html')
    # Получаем город от пользователя
    user_city = request.get_json().get('city', '').strip().upper()
    analyzer = Analyzer(user)
    response = analyzer.analyze_response(user_city)
    return make_response(response)
