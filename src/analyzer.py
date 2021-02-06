"""Модуль содержит определение класса Analyzer для обработки ответа
пользователя и формирования ответа сервера."""

from .searcher import Searcher


class Analyzer:
    """Класс для обработки ответа пользователя и формирования ответ."""

    # Ответ по умолчанию
    DEFAULT_RESPONSE = {
        'response': {'text': 'Повторите вопрос... Я ничего не поняла',
                     'tts': 'Повторите вопрос... Я ничего не поняла',
                     'end_session': False},
        'version': '1.0'}
    # Ответ
    response = {
        'response': {'text': 'Повторите вопрос... Я ничего не поняла',
                     'end_session': False},
        'version': '1.0'}

    def __init__(self, user=''):
        """Конструктор.
        :param user: идентификтор пользователя-игрока."""

        self.searcher = Searcher()
        self.user = user

    def analyze_response(self, text):
        """Функция анализирует ответ пользователя - название города.
        :param text: текст запроса от пользователя.
        :return: словарь с ответом в формате
        {text: текст ответа, end: True, если нужно завершить игру,
        status: статус ответа для сайта, letter: буква, на которую должно
        начинаться название следующего города}."""

        if not text:
            # Пользователь ничего не ответил
            text = 'Вы ничего не назвали.'
            return {'text': text, 'end': False, 'status': 1}

        if text in ('КАК ИГРАТЬ', 'ПРАВИЛА ИГРЫ'):
            # Правила игры
            text = (
                'Мы играем в Города. В игре каждый участник по очереди '
                'называет реально существующий город любой страны. Название '
                'города должно начинаться на букву, которой оканчивается '
                'название предыдущего города. Первым город называете вы. '
                'Название первого города может быть любым.')
            return {'text': text, 'end': False, 'status': 1}

        from .main import session_data
        # Проверяем, что пользователь ввел город на нужную букву
        letter = self.searcher.check_city_name(session_data.get(self.user, []),
                                               text)
        if letter:
            # Пользователь ввел название с неправильной буквы
            text = f'Ваш ответ {text} не начинается на нужную букву {letter}.'
            return {'text': text, 'end': False, 'status': 1}

        # Проверяем, что город еще не назывался
        if text in session_data.get(self.user, []):
            # Пользователь назвал город, который уже назывался в игре
            text = f'Город {text} уже назывался.'
            return {'text': text, 'end': False, 'status': 1}

        # Проверяем, что пользователь ввел город
        r = self.searcher.check_city(text)
        if not r.get('city'):
            # Пользователь ввел не название города
            text = f'Ваш ответ {text} не является названием города.'
            return {'text': text, 'end': False, 'status': 1}

        # Пользователь ввел название города
        user_city_info = r.get('info')
        session_data[self.user].append(text)
        # Находим город-ответ, начинающийся на последнюю букву города
        # пользователя
        letter = self.searcher.get_letter(text)
        r = self.searcher.find_city(letter, session_data[self.user])
        if not r.get('city'):
            # Не найдено название города
            text = (f'Вы назвали город {text} ({user_city_info}). Я больше '
                    f'не знаю городов на букву {letter}. Вы победили.')
            return {'text': text, 'end': True, 'status': 2}

        # Найдено название города для ответа
        city = r.get('city').strip().upper()
        city_info = r.get('info')
        session_data[self.user].append(city)
        letter = self.searcher.get_letter(city)
        text = (f'Вы назвали город {text} ({user_city_info}). Мой город {city}'
                f'({city_info}). Назовите город на букву {letter}.')
        return {'text': text, 'end': False, 'status': 3, 'letter': letter}

    def get_default(self):
        """Метод возвращает ответ по умолчанию."""

        return self.DEFAULT_RESPONSE

    def make_response_to_alice(self, user, text, new):
        """Метод создает ответ на запрос Алисы.
        :param user: идентификатор пользователя;
        :param text: сообщение запроса;
        :param new: если True, то сессия только что началась.
        :param response: ответ."""

        from .main import session_data
        self.user = user
        if new:
            # Это новый пользователь
            session_data.pop(self.user, None)
            session_data[self.user] = []
            self.response['response']['text'] = 'Привет! Назовите город.'
            # response['response']['buttons'] = self.get_suggests()
            return self.response
        # Обрабатываем ответ пользователя
        r = self.analyze_response(text)
        self.response['response']['text'] = r['text']
        self.response['response']['end_session'] = r['end']
        return self.response
