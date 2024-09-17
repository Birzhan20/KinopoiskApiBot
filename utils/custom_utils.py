import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger
from loader import UserStates
from states import user_states, STATES
from loader import bot

user_data: dict[int, dict[str, str]] = (
    {}
)  # Словарь для хранения данных пользователя


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES['WAITING_CUSTOM_GENRE'])
def handle_year_to(message: Message) -> None:
    user_id = message.from_user.id
    user_data[user_id] = {}

    if message.from_user.id in user_states:
        user_states.pop(message.from_user.id)

    user_states[message.from_user.id] = STATES['WAITING_CUSTOM_GENRE1']

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("2000")
    button2 = types.KeyboardButton("2010")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "От:", reply_markup=keyboard)



@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES['WAITING_CUSTOM_GENRE1'])
def handle_year_to(message: Message) -> None:
    """
    Обрабатывает год 'от', запрашивает год 'до' у пользователя.
    """
    user_id = message.from_user.id
    user_data[user_id]["from_year"] = message.text

    if message.from_user.id in user_states:
        user_states.pop(message.from_user.id)

    user_states[message.from_user.id] = STATES['WAITING_CUSTOM_GENRE2']

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("2015")
    button2 = types.KeyboardButton("2024")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "До:", reply_markup=keyboard)



@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES['WAITING_CUSTOM_GENRE2'])
def handle_country(message: Message) -> None:
    """
    Обрабатывает страну, запрашивает выбор страны у пользователя.
    """
    user_id = message.from_user.id
    user_data[user_id]["to_year"] = message.text

    if message.from_user.id in user_states:
        user_states.pop(message.from_user.id)

    user_states[message.from_user.id] = STATES['WAITING_CUSTOM_GENRE3']

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("russia")
    button2 = types.KeyboardButton("usa")
    button3 = types.KeyboardButton("kazakhstan")
    button4 = types.KeyboardButton("china")
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Страна:", reply_markup=keyboard)



@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == STATES['WAITING_CUSTOM_GENRE3'])
def handle_data(message: Message) -> None:
    """
    Обрабатывает данные пользователя, делает запрос к API и отправляет результаты пользователю.
    """
    user_id = message.from_user.id

    from_year = user_data[user_id].get("from_year")
    to_year = user_data[user_id].get("to_year")
    country = user_data[user_id].get("country")

    kinopoisk_api_key = os.getenv("KINOPOISK_API_KEY")
    url = f"https://api.kinopoisk.dev/v1.4/movie?premiere.{country}={from_year}-{to_year}&token={kinopoisk_api_key}"

    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if "docs" in data and data["docs"]:
                films = data["docs"]
                reply = "Фильмы за выбранный период и страну:\n"
                for film in films:
                    reply += f"- {film['name']} ({film['year']})\n"
                bot.reply_to(message, reply)
                logger.info("Успешно получены данные о фильмах.")
            else:
                bot.reply_to(message, "Не удалось найти данные.")
                logger.warning("Данные не найдены.")
        else:
            logger.error(
                f"Ошибка запроса: статус-код {res.status_code}, ответ: {res.text}"
            )
            bot.reply_to(message, f"Ошибка. Статус-код: {res.status_code}.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, "Ошибка при запросе данных.")
        logger.error(f"Ошибка при запросе данных: {e}")
    except Exception as e:
        bot.reply_to(message, "Произошла непредвиденная ошибка.")
        logger.exception(f"Непредвиденная ошибка: {e}")

    user_states.pop(message.from_user.id, None)
