"""Модуль содержит определение класса Analyzer для обработки ответа
пользователя и формирования ответа сервера."""

from .searcher import Searcher


class Analyzer:
    """Класс для обработки ответа пользователя и формирования ответ."""

    def __init__(self, session, user):
        """Конструктор.
        :param session: объект session из flask;
        :param user: идентификтор пользователя-игрока."""

        self.searcher = Searcher()
        self.session = session
        self.user = user

    def analyze_response(self, user_city):
        """Функция анализирует ответ пользователя - название города.
        :param user_city: название города от пользователя.
        :return: словарь с ответом в формате
        {text: текст ответа, end: True, если нужно завершить игру,
        status: статус ответа для сайта, letter: буква, на которую должно
        начинаться название следующего города}."""

        if not user_city:
            # Пользователь ничего не ответил
            text = 'Вы ничего не назвали'
            return {'text': text, 'end': False, 'status': 1}

        from .main import session_data
        # Проверяем, что пользователь ввел город на нужную букву
        letter = self.searcher.check_city_name(session_data.get(self.user, []),
                                               user_city)
        if letter:
            # Пользователь ввел название с неправильной буквы
            text = f'Ваш ответ {user_city} не начинается на нужную букву {letter}'
            return {'text': text, 'end': False, 'status': 1}

        # Проверяем, что город еще не назывался
        if user_city in session_data.get(self.user, []):
            # Пользователь назвал город, который уже назывался в игре
            text = f'Город {user_city} уже назывался'
            return {'text': text, 'end': False, 'status': 1}

        # Проверяем, что пользователь ввел город
        r = self.searcher.check_city(user_city)
        if not r.get('city'):
            # Пользователь ввел не название города
            text = f'Ваш ответ {user_city} не является названием города'
            return {'text': text, 'end': False, 'status': 1}

        # Пользователь ввел название города
        user_city_info = r.get('info')
        session_data[self.user].append(user_city)
        # Находим город-ответ, начинающийся на последнюю букву города
        # пользователя
        letter = self.searcher.get_letter(user_city)
        r = self.searcher.find_city(letter, session_data[self.user])
        if not r.get('city'):
            # Не найдено название города
            text = f'Вы назвали город {user_city} ({user_city_info}). '
            text += f'Я больше не знаю городов на букву {letter}.'
            text += 'Вы победили'
            return {'text': text, 'end': True, 'status': 2}

        # Найдено название города для ответа
        city = r.get('city').strip().upper()
        city_info = r.get('info')
        session_data[self.user].append(city)
        letter = self.searcher.get_letter(city)
        text = f'Вы назвали город {user_city} ({user_city_info}). '
        text += f'Мой город {city} ({city_info}). Назовите город на букву {letter}'
        return {'text': text, 'end': False, 'status': 3, 'letter': letter}

    def make_response_to_alice(self, user_city, new, response):
        """Метод создает ответ на запрос Алисы.
        :param user_city: название города от пользователя;
        :param new: если True, то сессия только что началась.
        :param response: ответ."""

        from .main import session_data
        if new:
            # Это новый пользователь
            self.session.clear()
            session_data.pop(self.user, None)
            session_data[self.user] = []
            self.session['user'] = self.user
            response['response']['text'] = 'Привет! Назовите город'
            #response['response']['buttons'] = self.get_suggests()
            return
        # Обрабатываем ответ пользователя
        r = self.analyze_response(user_city)
        response['response']['text'] = r['text']
        response['session']['end_session'] = r['end']
