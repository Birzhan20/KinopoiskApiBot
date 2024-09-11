from telebot.types import Message
from loguru import logger

from utils.history_utils import save_data
from loader import bot

logger.add("bot_start.log", rotation="10 MB", compression="zip")


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    """
    Обрабатывает команду '/start' и отправляет приветственное сообщение пользователю.

    Args:
        message (Message): Сообщение от пользователя с командой '/start'.
    """
    save_data(text=message.text, username=message.from_user.username)
    logger.info(f"Обработка '/start'")

    bot.reply_to(
        message,
        f"Привет, {message.from_user.full_name}!\n"
        f"Данный бот подберет вам фильмы!\n"
        f"/help - инструкция.",
    )
