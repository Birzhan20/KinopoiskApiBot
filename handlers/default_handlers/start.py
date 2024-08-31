from telebot.types import Message
from loguru import logger
from loader import bot

logger.add("bot_start.log", rotation="10 MB", compression="zip")


@bot.message_handler(commands=["start"])
def start(message: Message):
    logger.info(f"Обработка '/start'")
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"Данный бот подберет вам фильмы!\n"
                          f"/help - инструкция.")
