"""Модуль содержит определение класса Searcher для поиска информации о городе
в интернете."""

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


class Searcher:
    """Класс для поиска городов."""

    # Словарь для перехода от кириллических букв к латинским
    _LETTERS = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
        'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'YI', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH',
        'Э': 'YE', 'Ю': 'YU', 'Я': 'YA'}
    # Будем искать данные на сайте Planetolog.ru
    _URL = 'http://www.planetolog.ru/city-world-alphabet.php?abc='
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 \
            Safari/537.36'}

    def __init__(self):
        """Конструктор класса."""

        pass

    def check_city(self, word):
        """Метод проверяет, является ли слово названием города.
        :param word: проверяемое слово.
        :return: словарь в формате {city: True/False, info: информация}.
        Если city = True, то проверяемое слово - название города."""

        # Ищем города с первой буквой из слова word
        letter = self._LETTERS.get(word[0].upper(), '')
        for city in self.find_cities(letter):
            if city.string.upper() == word.upper():
                # Нашли город, получаем информацию о нем
                url = urljoin(self._URL, city.get('href'))
                info = self.get_city_info(url)
                return {'city': True, 'info': info}
        return {'city': False}

    def check_city_name(self, used_cities, city):
        """Метод проверяет, что название города city начинается с последней
        буквы города из списка used_cities.
        :param used_cities: список использованных названий городов;
        :param city: названия городов.
        :return: буква, на которую должно начинаться название города, или
        None."""

        if not used_cities:
            return None
        first_letter = city[0].upper()
        last_letter = self.get_letter(used_cities[-1])
        if first_letter == last_letter:
            return None
        return last_letter

    def find_cities(self, letter):
        """Метод ищет города по первой букве.
        :param letter: первая буква в названии города.
        :return: список городов с первой заданной буквой."""

        # По первой букве города на латинице формируем адрес запроса
        url = f'{self._URL}{letter}'
        r = requests.get(url, headers=self._HEADERS)
        if r.status_code != 200:
            # Не удалось получить ответ
            return []
        # Обрабатываем ответ
        soup = bs(r.text, 'lxml')
        cities = soup.find_all('td', attrs={'class': 'CountryList'})
        if len(cities) != 2:
            # Нет городов, начинающихся с заданной буквы
            return []
        # Возвращаем список городов, начинающихся с заданной буквы
        return cities[1].find_all('a')

    def find_city(self, letter, used_cities):
        """Метод ищет город по первой букве в названии.
        :param letter: первая буква в названии города;
        :param used_cities: список названий городов, использованных в игре.
        :return: словарь {city: название города, info: информация} с названием
        и информацией найденного города."""

        # Ищем города по первой букве
        letter = self._LETTERS.get(letter.upper(), '')
        for city in self.find_cities(letter):
            if city.string.upper() not in used_cities:
                # Нашли название города, ранее не использованное в игре
                url = urljoin(self._URL, city.get('href'))
                info = self.get_city_info(url)
                return {'city': city.string.upper(), 'info': info}
        return {'city': False}

    def get_city_info(self, url):
        """Метод получает информацию о городе.
        :param url: ссылка на страницу с информацией.
        :return: текст информации."""

        r = requests.get(url, headers=self._HEADERS)
        if r.status_code != 200:
            # Не удалось получить ответ
            return None
        # Обрабатываем ответ
        soup = bs(r.text, 'lxml')
        spam = soup.find_all(name='div', attrs={'class': 'textplane'})
        if len(spam) != 3:
            return None
        # Возвращаем первое предложение из абзаца
        info = spam[1].find('p').contents[0].strip()
        i = info.find('.')
        return info[:i]

    def get_letter(self, word):
        """Метод возвращает последнюю букву, с которой может начинаться
        название города.
        :param word: название города.
        :return: буква."""

        reversed_word = word[::-1].upper()
        for letter in reversed_word:
            if self._LETTERS.get(letter, None):
                return letter
        return None


if __name__ == '__main__':
    # Промоделируем игру компьютера самого с собой
    searcher = Searcher()
    used_cities = []
    first_city = 'Якутск'
    s = searcher.check_city(first_city)
    if s['city']:
        print(f"{first_city} - {s['info']}")
    city = first_city.upper()
    i = 0
    while city or i < 10:
        used_cities.append(city)
        letter = searcher.get_letter(city)
        s = searcher.find_city(letter, used_cities)
        city = s['city'].upper()
        print(f'{city} - {s["info"]}')
        i += 1
