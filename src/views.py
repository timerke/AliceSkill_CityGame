"""Модуль с функциями представления при работе с пользователем сайта."""

from flask import (Blueprint, flash, make_response, redirect, render_template,
                   request, session, url_for)
#from .main import session_data
from .searcher import Searcher


bp = Blueprint('site', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    """Функция представления обрабатывает на исходной странице."""

    if request.method == 'POST':
        # Получаем ip адрес пользователя и сохраняем его
        user = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        session.clear()
        session['user'] = user
        return render_template('game.html', start=True)
    # Ответ на метод GET
    return render_template('index.html')


@bp.route('/game', methods=('GET', 'POST'))
def game():
    """Функция представления обрабатывает запросы на странице с игрой."""

    if request.method == 'POST':
        user = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if session.get('user') != user:
            return render_template('index.html')
        # Получаем город от пользователя
        user_city = request.get_json().get('city')
        if not user_city:
            # Пользователь ничего не ввел
            data = {'status': 1,
                    'text': 'Вы не ввели название города'}
            return make_response(data)
        # Проверяем, что пользователь ввел город
        searcher = Searcher()
        user_city = user_city.strip().upper()
        r = searcher.check_city(user_city)
        if not r.get('city'):
            # Пользователь ввел не название города
            data = {'status': 2,
                    'text': f'Ваш ответ {user_city} не является названием города'}
            return make_response(data)
        # Пользователь ввел название города
        from .main import session_data
        user_city_info = r.get('info')
        session_data.append(user_city)
        # Находим город-ответ, начинающийся на последнюю букву города
        # пользователя
        letter = searcher.get_letter(user_city)
        r = searcher.find_city(letter, session_data)
        if not r.get('city'):
            # Не найдено название города
            data = {'status': 3, 'user_city': user_city,
                    'user_city_info': user_city_info,
                    'text': f'Я больше не знаю городов на букву {letter}'}
            return make_response(data)
        # Найдено название города для ответа
        city = r.get('city').upper()
        city_info = r.get('info')
        session_data.append(city)
        data = {'status': 4, 'user_city': user_city,
                'user_city_info': user_city_info, 'city': city,
                'city_info': city_info, 'letter': searcher.get_letter(city)}
        print(data)
        return make_response(data)
    return render_template('game.html')


@bp.route('/finish', methods=('POST',))
def finish():
    """Функция представления обрабатывает запрос завершения игры."""

    from .main import session_data
    session.clear()
    session_data = []
    return redirect(url_for('site.index'))
