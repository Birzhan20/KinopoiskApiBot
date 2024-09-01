from loguru import logger
from database.data import History, save_data
from loader import bot
from telebot.types import Message

logger.add("bot_history.log", rotation="1 MB", compression="zip")


@bot.message_handler(commands=["history"])
def history(message: Message) -> None:
    """
    Обрабатывает команду '/history' и отправляет пользователю последние 10 запросов из истории.

    Args:
        message (Message): Сообщение от пользователя с командой '/history'.
    """
    save_data(text="/history", username=message.from_user.username)
    logger.info(f"Обработка '/history'")

    try:
        # Получение последних 10 записей из истории
        recent_history = (
            History.select().order_by(History.date.desc()).limit(10)
        )
        history_entries = [
            (
                f"Пользователь: {entry.user.username}, "
                f"Дата: {entry.date.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Запрос: {entry.content}"
            )
            for entry in recent_history
        ]
        result = "\n".join(history_entries)

        # Отправка истории пользователю
        bot.send_message(message.from_user.id, result)

    except Exception as e:
        logger.error(f"Ошибка при обработке команды '/history': {e}")
        bot.send_message(
            message.from_user.id, "Произошла ошибка при получении истории."
        )
