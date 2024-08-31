from telebot.types import Message
from loguru import logger
from loader import bot
from database.data import save_data

from .high import high
from .custom import custom
from .low import low
from .start import start
from .help import help
from .history import history

logger.add("bot_echo.log", rotation="1 MB", compression="zip")


@bot.message_handler(state=None)
def bot_echo(message: Message):

    if message.text == '/high':
        logger.info(f"Выполнение '/high'")
        save_data(message.text)
        bot.register_next_step_handler(message, high)

    elif message.text == '/low':
        bot.register_next_step_handler(message, low)
        logger.info(f"Выполнение '/low'")

    elif message.text == '/custom':
        bot.register_next_step_handler(message, custom)
        logger.info(f"Выполнение '/custom'")

    elif message.text == '/help':
        bot.register_next_step_handler(message, help)
        logger.info(f"Выполнение '/help'")

    elif message.text == '/history':
        bot.register_next_step_handler(message, history)
        logger.info(f"Выполнение '/history'")

    elif message.text == '/start':
        bot.register_next_step_handler(message, start)
        logger.info(f"Выполнение '/start'")

    elif message.text == '/Hello world!' or message.text == 'Привет':
        bot.reply_to(message, "You are welcome!")
        logger.info(f"Greetings")

    else:
        bot.reply_to(
            message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
        )
        logger.info(f"Empty echo")
