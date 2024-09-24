import os
import requests
from telebot import types
from telebot.types import Message
from loguru import logger
from database.save_data import save_data
from loader import bot
from telebot.states import State, StatesGroup
from telebot import custom_filters

logger.add("bot_low.log", rotation="1 MB", compression="zip")


class LowGenreStates(StatesGroup):
    low_genre = State()


@bot.message_handler(commands=["low"])
def low(message: Message) -> None:
    """
    Обрабатывает команду '/low' и отправляет пользователю список фильмов с минимальным рейтингом
    в выбранном жанре.

    Args:
        message (Message): Сообщение от пользователя с командой '/low'.
    """
    save_data(text=message.text, username=message.from_user.username)

    logger.info(
        f"Получена команда '/low' от пользователя {message.from_user.id}"
    )

    bot.set_state(message.from_user.id, LowGenreStates.low_genre, message.chat.id)
    bot.send_message(message.chat.id, "Выберите жанр:")


@bot.message_handler(state=LowGenreStates.low_genre)
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
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))

