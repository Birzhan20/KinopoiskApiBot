from telebot.types import Message
from loguru import logger
from config_data.config import DEFAULT_COMMANDS
from loader import bot

logger.add("bot_help.log", rotation="10 MB", compression="zip")


@bot.message_handler(commands=["help"])
def help(message: Message):
    logger.info(f"Обработка '/help'")
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
