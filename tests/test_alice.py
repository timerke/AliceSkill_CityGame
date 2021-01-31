"""Модуль содержит тесты запросов."""

import re
from src.main import session_data

user_id = "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8"


def test_hello(client):
    response = client.get('/hello/world')
    assert response.data == b'Hello, WORLD!'


def test_1(client):
    """Если получен неверный формат запроса."""

    response = client.post('alice/')
    assert response.get_json() == {'info': 'Неверный формат запроса'}


def test_2(client):
    """Если получен запрос на начало игры."""

    # Данные в запросе
    REQUEST = {
        "request": {
            "original_utterance": "",
        },
        "session": {
            "message_id": 0,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": user_id,
            "user": {
                "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
            },
            "application": {
                "application_id": user_id
            },
            "new": True
        },
        "version": "1.0"
    }
    # Правильный ответ на запрос
    RESPONSE = {
        'response': {'text': 'Привет! Назовите город'},
        'version': REQUEST.get('version'),
        'session': REQUEST.get('session'),
        'session': {'end_session': False}
    }
    response = client.post('alice/', json=REQUEST)
    print(response.get_json())
    assert response.get_json() == RESPONSE


def test_3(client):
    """Если получен запрос с названием города от пользователя."""

    # Данные в запросе
    REQUEST = {
        "request": {
            "original_utterance": "Якутск",
        },
        "session": {
            "message_id": 1,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": user_id,
            "user": {
                "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
            },
            "application": {
                "application_id": user_id
            },
            "new": False
        },
        "version": "1.0"
    }
    # Правильный ответ на запрос
    RESPONSE = {
        'response': {'text': 'К'},
        'version': REQUEST.get('version'),
        'session': REQUEST.get('session'),
        'session': {'end_session': False}
    }
    response = client.post('alice/', json=REQUEST).get_json()
    text = response['response']['text']
    first_letter = re.search(r'Мой город [А-Я]', text).group(0)[-1]
    response['response']['text'] = first_letter
    assert response == RESPONSE


def test_4(client):
    """Если получен запрос с пустым ответом от пользователя."""

    # Данные в запросе
    REQUEST = {
        "request": {
            "original_utterance": "",
        },
        "session": {
            "message_id": 1,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": user_id,
            "user": {
                "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
            },
            "application": {
                "application_id": user_id
            },
            "new": False
        },
        "version": "1.0"
    }
    # Правильный ответ на запрос
    RESPONSE = {
        'response': {'text': 'Вы ничего не назвали'},
        'version': REQUEST.get('version'),
        'session': REQUEST.get('session'),
        'session': {'end_session': False}
    }
    response = client.post('alice/', json=REQUEST).get_json()
    assert response == RESPONSE


def test_5(client):
    """Если получен запрос с ответом от пользователя, в котором указано
    название, которое не принадлежит городу."""

    # Данные в запросе
    last_letter = get_letter()
    REQUEST = {
        "request": {
            "original_utterance": last_letter + "рвыорк",
        },
        "session": {
            "message_id": 1,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": user_id,
            "user": {
                "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
            },
            "application": {
                "application_id": user_id
            },
            "new": False
        },
        "version": "1.0"
    }
    # Правильный ответ на запрос
    RESPONSE = {
        'response': {'text': f'Ваш ответ {last_letter + "РВЫОРК"} не является названием города'},
        'version': REQUEST.get('version'),
        'session': REQUEST.get('session'),
        'session': {'end_session': False}
    }
    response = client.post('alice/', json=REQUEST).get_json()
    assert response == RESPONSE


def test_6(client):
    """Если получен запрос с ответом от пользователя, в котором указано
    название города с неправильной буквы."""

    # Данные в запросе
    city = get_city()
    letter = get_letter()
    REQUEST = {
        "request": {
            "original_utterance": city,
        },
        "session": {
            "message_id": 1,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": user_id,
            "user": {
                "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
            },
            "application": {
                "application_id": user_id
            },
            "new": False
        },
        "version": "1.0"
    }
    # Правильный ответ на запрос
    RESPONSE = {
        'response': {'text': f'Ваш ответ {city} не начинается на нужную букву {letter}'},
        'version': REQUEST.get('version'),
        'session': REQUEST.get('session'),
        'session': {'end_session': False}
    }
    response = client.post('alice/', json=REQUEST).get_json()
    assert response == RESPONSE


def get_letter():
    """Функция возвращает последнюю букву слова, на которую может начинаться
    следующее слово.
    :return: последняя буква."""

    word = session_data[user_id][-1]
    reversed_word = word[::-1]
    for letter in reversed_word:
        if letter not in ('Ы', 'Ь', 'Ъ'):
            return letter


def get_city():
    """Функция возвращает название города с неправильной буквы.
    :return: название города."""

    last_letter = get_letter()
    if last_letter == 'В':
        return 'Элиста'.upper()
    return 'Владивосток'.upper()
