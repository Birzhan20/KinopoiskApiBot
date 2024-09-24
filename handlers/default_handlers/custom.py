import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger
from loader import bot
from database.save_data import save_data
from telebot import custom_filters
from telebot.states import State, StatesGroup
from telebot.storage import StateMemoryStorage

# Логирование
logger.add("bot_custom.log", rotation="1 MB", compression="zip")

# Инициализация хранилища состояний
state_storage = StateMemoryStorage()

# Определяем группы состояний для пользователя
class CustomGenreStates(StatesGroup):
    year_from = State()  # Состояние для года "от"
    year_to = State()  # Состояние для года "до"
    country = State()  # Состояние для выбора страны


# Стартовое сообщение для кастомного выбора жанров
@bot.message_handler(commands=["custom"])
def custom(message: Message) -> None:
    save_data(text=message.text, username=message.from_user.username)
    bot.set_state(message.from_user.id, CustomGenreStates.year_from, message.chat.id)
    bot.reply_to(message, "Выберите диапазон по годам. Укажите 'от':")


# Обработка года "от"
@bot.message_handler(state=CustomGenreStates.year_from)
def handle_year_from(message: Message) -> None:
    # Сохраняем данные в хранилище состояний
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["from_year"] = message.text

    bot.set_state(message.from_user.id, CustomGenreStates.year_to, message.chat.id)
    bot.send_message(message.chat.id, "Теперь укажите 'до':")


# Обработка года "до"
@bot.message_handler(state=CustomGenreStates.year_to)
def handle_year_to(message: Message) -> None:
    # Сохраняем данные в хранилище состояний
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["to_year"] = message.text

    bot.set_state(message.from_user.id, CustomGenreStates.country, message.chat.id)
    bot.send_message(message.chat.id, "Введите страну:")


# Обработка страны и отправка запроса к API
@bot.message_handler(state=CustomGenreStates.country)
def handle_country(message: Message) -> None:
    # Сохраняем страну в хранилище состояний
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["country"] = message.text
        from_year = data.get("from_year")
        to_year = data.get("to_year")
        country = data.get("country")

    # Делаем запрос к API
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
            else:
                bot.reply_to(message, "Не удалось найти данные.")
        else:
            bot.reply_to(message, f"Ошибка. Статус-код: {res.status_code}.")
    except requests.exceptions.RequestException:
        bot.reply_to(message, "Ошибка при запросе данных.")
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)


# Добавляем фильтр состояний
bot.add_custom_filter(custom_filters.StateFilter(bot))
