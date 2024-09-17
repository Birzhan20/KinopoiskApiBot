import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger
from utils.history_utils import save_data
from loader import bot
from utils.high_utils import get_max_genre
from states import user_states, STATES

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

    if message.from_user.id in user_states:
        user_states.pop(message.from_user.id)

    user_states[message.from_user.id] = STATES['WAITING_HIGH_GENRE']

    # Создает клавиатуру с жанрами
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("драма")
    button2 = types.KeyboardButton("аниме")
    button3 = types.KeyboardButton("криминал")
    button4 = types.KeyboardButton("спорт")
    keyboard.add(button1, button2, button3, button4)

    # Отправляет сообщение пользователю с запросом на выбор жанра
    bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=keyboard)
