import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger
from utils.custom_utils import handle_data, handle_country, handle_year_to
from loader import UserStates
from telebot.storage import StateMemoryStorage

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

    bot.delete_state(user_id, message.chat.id)

    logger.info(f"Получена команда '/custom' от пользователя {user_id}")

    bot.reply_to(message, "Выберите диапазон по годам.")

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("2000")
    button2 = types.KeyboardButton("2010")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "От:", reply_markup=keyboard)
    bot.set_state(user_id, UserStates.waiting_for_from_year, message.chat.id)
