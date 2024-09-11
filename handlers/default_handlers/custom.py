import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger
from utils.custom_utils import handle_data, handle_country, handle_year_to

from utils.history_utils import save_data
from loader import bot

logger.add("bot_custom.log", rotation="1 MB", compression="zip")

user_data: dict[int, dict[str, str]] = (
    {}
)  # Словарь для хранения данных пользователя


@bot.message_handler(commands=["custom"])
def custom(message: Message) -> None:
    """
    Обрабатывает команду '/custom', запрашивает диапазон по годам и страну у пользователя.
    """
    save_data(text=message.text, username=message.from_user.username)
    user_id = message.from_user.id
    user_data[user_id] = {}

    logger.info(f"Получена команда '/custom' от пользователя {user_id}")

    bot.reply_to(message, "Выберите диапазон по годам.")

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("2000")
    button2 = types.KeyboardButton("2010")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "От:", reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_year_to)
