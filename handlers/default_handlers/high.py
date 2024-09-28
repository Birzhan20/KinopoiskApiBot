import requests
from telebot.types import Message
import os
from loguru import logger
from database.save_data import save_data
from loader import bot
from telebot import custom_filters
from states.state_high import HighGenreStates
from config_data.config import KINOPOISK_API_KEY


logger.add("bot_high.log", rotation="1 MB", compression="zip")


@bot.message_handler(commands=["high"])
def high(message: Message) -> None:
    """
    Обрабатывает команду '/high' и предлагает пользователю выбрать жанр для поиска фильмов с высоким рейтингом.

    Args:
        message (Message): Сообщение от пользователя с командой '/high'.
    """
    # Сохраняет данные о запросе в базе
    save_data(text=message.text, username=message.from_user.username)

    # Логгирует получение команды
    logger.info(
        f"Получена команда '/high' от пользователя {message.from_user.id}"
    )

    bot.set_state(message.from_user.id, HighGenreStates.high_genre, message.chat.id)
    bot.send_message(message.chat.id, "Введите жанр:")


@bot.message_handler(state=HighGenreStates.high_genre)
def get_max_genre(message: Message) -> None:
    """
    Обрабатывает выбранный пользователем жанр и запрашивает данные о фильмах с максимальным рейтингом в указанном жанре.

    Args:
        message (Message): Сообщение от пользователя с выбранным жанром.
    """
    genre = message.text
    logger.info(f"Запуск запроса по жанру {genre}.")

    # Формирует URL для запроса к API
    url = f"https://api.kinopoisk.dev/v1.4/movie?rating.imdb=8-10&genres.name={genre}&token={KINOPOISK_API_KEY}"

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
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)

bot.add_custom_filter(custom_filters.StateFilter(bot))
