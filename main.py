from loguru import logger
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands

logger.add("bot.log", rotation="10 MB", compression="zip")

if __name__ == "__main__":
    try:
        logger.info("Запуск бота")
        set_default_commands(bot)
        bot.infinity_polling()
    except Exception as e:
        logger.exception("Ошибка при запуске бота:")
