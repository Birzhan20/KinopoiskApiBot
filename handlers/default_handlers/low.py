import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger

from loader import bot

logger.add("bot_low.log", rotation="1 MB", compression="zip")


@bot.message_handler(commands=["low"])
def low(message: Message):

    logger.info(f"Получена команда '/low' от пользователя {message.from_user.id}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("драма")
    button2 = types.KeyboardButton("аниме")
    button3 = types.KeyboardButton("криминал")
    button4 = types.KeyboardButton("спорт")
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_min_genre)


def get_min_genre(message: Message):
    kinopoisk_api_key = os.getenv('KINOPOISK_API_KEY')
    genre = message.text
    logger.info(f"Запуск запроса по жанру.")

    url = f'https://api.kinopoisk.dev/v1.4/movie?rating.imdb=2-5&genres.name={genre}&&token={kinopoisk_api_key}'

    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            print(data)
            if "docs" in data and data["docs"]:
                films = data["docs"]
                reply = f'Фильмы с минимальным рейтингом в жанре {genre}:\n'
                for film in films:
                    reply += f"- {film['name']} ({film['year']})\n"
                bot.reply_to(message, reply)
                logger.info(f"Успешно получены данные о фильмах.")
            else:
                bot.reply_to(message, f'Не удалось найти данные.')
                logger.warning(f"Данные не найдены.")
        else:
            logger.error(
                f"Ошибка запроса /low: статус-код {res.status_code}, ответ: {res.text}")
            bot.reply_to(message, f'Ошибка. Статус-код: {res.status_code}.')
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f'Ошибка при запросе данных.')
        logger.error(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        bot.reply_to(message, "Произошла непредвиденная ошибка.")
        logger.exception(f"Непредвиденная ошибка: {e}")

