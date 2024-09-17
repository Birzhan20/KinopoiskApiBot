import requests
from telebot.types import Message
import os
from loguru import logger
from states import user_states, STATES
from loader import bot


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES['WAITING_LOW_GENRE'])
def get_min_genre(message: Message) -> None:
    """
    Обрабатывает выбранный жанр и запрашивает фильмы с минимальным рейтингом в этом жанре.

    Args:
        message (Message): Сообщение от пользователя с выбранным жанром.
    """
    kinopoisk_api_key = os.getenv("KINOPOISK_API_KEY")
    genre = message.text
    logger.info("Запуск запроса по жанру.")

    url = f"https://api.kinopoisk.dev/v1.4/movie?rating.imdb=2-5&genres.name={genre}&&token={kinopoisk_api_key}"

    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if "docs" in data and data["docs"]:
                films = data["docs"]
                reply = f"Фильмы с минимальным рейтингом в жанре {genre}:\n"
                for film in films:
                    reply += f"- {film['name']} ({film['year']})\n"
                bot.reply_to(message, reply)
                logger.info("Успешно получены данные о фильмах.")
            else:
                bot.reply_to(message, "Не удалось найти данные.")
                logger.warning("Данные не найдены.")
        else:
            logger.error(
                f"Ошибка запроса /low: статус-код {res.status_code}, ответ: {res.text}"
            )
            bot.reply_to(message, f"Ошибка. Статус-код: {res.status_code}.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, "Ошибка при запросе данных.")
        logger.error(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        bot.reply_to(message, "Произошла непредвиденная ошибка.")
        logger.exception(f"Непредвиденная ошибка: {e}")

    user_states.pop(message.from_user.id, None)
