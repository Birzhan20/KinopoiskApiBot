from telebot.types import Message
from loguru import logger
from config_data.config import DEFAULT_COMMANDS
from database.save_data import save_data
from loader import bot

logger.add("bot_help.log", rotation="10 MB", compression="zip")


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:
    """
    Обрабатывает команду '/help' и отправляет пользователю список доступных команд.

    Args:
        message (Message): Сообщение от пользователя с командой '/help'.
    """
    save_data(text=message.text, username=message.from_user.username)

    logger.info("Обработка '/help'")

    text = [
        f"/{command} - {description}"
        for command, description in DEFAULT_COMMANDS
    ]

    bot.reply_to(message, "\n".join(text))
