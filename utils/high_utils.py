import requests
from telebot.types import Message
import os
from loguru import logger
from loader import bot


def get_max_genre(message: Message) -> None:
    """
    Обрабатывает выбранный пользователем жанр и запрашивает данные о фильмах с максимальным рейтингом в указанном жанре.

    Args:
        message (Message): Сообщение от пользователя с выбранным жанром.
    """
    # Получает API ключ и жанр
    kinopoisk_api_key = os.getenv("KINOPOISK_API_KEY")
    genre = message.text
    logger.info(f"Запуск запроса по жанру {genre}.")

    # Формирует URL для запроса к API
    url = f"https://api.kinopoisk.dev/v1.4/movie?rating.imdb=8-10&genres.name={genre}&token={kinopoisk_api_key}"

    try:
        # Выполняет запрос к API
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if "docs" in data and data["docs"]:
                films = data["docs"]
                reply = f"Фильмы с максимальным рейтингом в жанре {genre}:\n"
                for film in films:
                    reply += f"- {film['name']} ({film['year']})\n"
                bot.reply_to(message, reply)
                logger.info("Успешно получены данные о фильмах.")
            else:
                bot.reply_to(message, "Не удалось найти данные.")
                logger.warning("Данные не найдены.")
        else:
            logger.error(
                f"Ошибка запроса /high: статус-код {res.status_code}, ответ: {res.text}"
            )
            bot.reply_to(message, f"Ошибка. Статус-код: {res.status_code}.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, "Ошибка при запросе данных.")
        logger.error(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        bot.reply_to(message, "Произошла непредвиденная ошибка.")
        logger.exception(f"Непредвиденная ошибка: {e}")
