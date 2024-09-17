from telebot import types
from telebot.types import Message
from loguru import logger

from utils.history_utils import save_data
from loader import bot
from states import user_states, STATES

logger.add("bot_low.log", rotation="1 MB", compression="zip")


@bot.message_handler(commands=["low"])
def low(message: Message) -> None:
    """
    Обрабатывает команду '/low' и отправляет пользователю список фильмов с минимальным рейтингом
    в выбранном жанре.

    Args:
        message (Message): Сообщение от пользователя с командой '/low'.
    """
    save_data(text=message.text, username=message.from_user.username)

    logger.info(
        f"Получена команда '/low' от пользователя {message.from_user.id}"
    )

    if message.from_user.id in user_states:
        user_states.pop(message.from_user.id)

    user_states[message.from_user.id] = STATES['WAITING_LOW_GENRE']

    # Создание клавиатуры для выбора жанра
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    button1 = types.KeyboardButton("драма")
    button2 = types.KeyboardButton("аниме")
    button3 = types.KeyboardButton("криминал")
    button4 = types.KeyboardButton("спорт")
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=keyboard)



