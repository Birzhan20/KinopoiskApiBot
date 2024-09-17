import requests
from telebot import types
from telebot.types import Message
import os
from loguru import logger
from utils.custom_utils import handle_data, handle_country, handle_year_to
from states import STATES, user_states

from utils.history_utils import save_data
from loader import bot

logger.add("bot_custom.log", rotation="1 MB", compression="zip")


@bot.message_handler(commands=["custom"])
def custom(message: Message) -> None:
    """
    Обрабатывает команду '/custom', запрашивает диапазон по годам и страну у пользователя.
    """
    save_data(text=message.text, username=message.from_user.username)
    user_id = message.from_user.id

    logger.info(f"Получена команда '/custom' от пользователя {user_id}")

    if message.from_user.id in user_states:
        user_states.pop(message.from_user.id)

    user_states[message.from_user.id] = STATES['WAITING_CUSTOM_GENRE']

    bot.reply_to(message, "Выберите диапазон по годам.")
