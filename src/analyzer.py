from .searcher import Searcher


class Analyzer:
    """Класс для обработки ответа пользователя и формирования ответ."""

    def __init__(self):

        self.searcher = Searcher()

    def analyze_response(user_city):
        """Функция анализирует ответ пользователя - название города.
        :param user_city: название города от пользователя."""

        if not user_city:
            # Пользователь ничего не ответил
            text = 'Вы ничего не назвали. Назовите город'
            return text, False

        from .main import session_data
        # Проверяем, что пользователь ввел город на нужную букву
        letter = self.searcher.check_city_name(session_data, user_city)
        if letter:
            # Пользователь ввел название с неправильной буквы
            text = f'Ваш ответ {user_city} не начинается на нужную букву {letter}'
            return text, False

        # Проверяем, что пользователь ввел город
        r = self.searcher.check_city(user_city)
        if not r.get('city'):
            # Пользователь ввел не название города
            text = f'Ваш ответ {user_city} не является названием города'
            return text, False

        # Пользователь ввел название города
        user_city_info = r.get('info')
        session_data.append(user_city)
        # Находим город-ответ, начинающийся на последнюю букву города
        # пользователя
        letter = self.searcher.get_letter(user_city)
        r = self.searcher.find_city(letter, session_data)
        if not r.get('city'):
            # Не найдено название города
            text = f'Вы назвали город {user_city} ({user_city_info}). '
            text += f'Я больше не знаю городов на букву {letter}.'
            text += 'Вы победили'
            return text, True

        # Найдено название города для ответа
        city = r.get('city').upper()
        city_info = r.get('info')
        session_data.append(city)
        letter = self.searcher.get_letter(city)
        text = f'Вы назвали город {user_city} ({user_city_info}). '
        text += f'Мой город {city} ({city_info}). Назовите город на букву {letter}'
        return text, False

    def make_response(self, data, response):
        """Функция создает ответ на запрос Алисы.
        :param data: данные из запроса Алисы;
        :param response: ответ."""

        from .main import session_data
        self.user_id = data['session']['user_id']
        if data['session']['new']:
            # Это новый пользователь
            session.clear()
            session_data = []
            session['user'] = self.user_id
            response['response']['text'] = 'Привет! Назовите город'
            #response['response']['buttons'] = self.get_suggests()
            return
        # Обрабатываем ответ пользователя
        user_city = data['request']['original_utterance'].strip().upper()
        response['response']['text'], response['session']['end_session'] =\
            self.analyze_response(user_city)
        return response
