from loguru import logger
from database.data import History
from loader import bot
from telebot.types import Message
from database.data import User

logger.add("bot_history.log", rotation="1 MB", compression="zip")


@bot.message_handler(commands=["history"])
def history(request):
    logger.info(f"Обработка '/history'")
    try:
        recent_history = History.select().order_by(History.date.desc()).limit(10)
        history_entries = [
            f"User: {entry.user.username}, Date: {entry.date}, Content: {entry.content}"
            for entry in recent_history
        ]
        result = "\n".join(history_entries)

        bot.send_message(request.from_user.id, result)

    except Exception as e:
        logger.error(f"Ошибка при обработке команды '/history': {e}")
        bot.send_message(request.from_user.id, "Произошла ошибка при получении истории.")
