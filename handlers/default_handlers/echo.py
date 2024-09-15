# from telebot.types import Message
# from loguru import logger
# from loader import bot
#
# from .high import high
# from .custom import custom
# from .low import low
# from .start import start
# from .help import help
# from .history import history
#
# logger.add("bot_echo.log", rotation="1 MB", compression="zip")
#
#
# @bot.message_handler(state=None)
# def bot_echo(message: Message) -> None:
#     """
#     Обрабатывает сообщения и перенаправляет их к соответствующим обработчикам команд.
#     """
#     if message.text == "/high":
#         logger.info("Выполнение '/high'")
#         bot.register_next_step_handler(message, high)
#
#     elif message.text == "/low":
#         logger.info("Выполнение '/low'")
#         bot.register_next_step_handler(message, low)
#
#     elif message.text == "/custom":
#         logger.info("Выполнение '/custom'")
#         bot.register_next_step_handler(message, custom)
#
#     elif message.text == "/help":
#         logger.info("Выполнение '/help'")
#         bot.register_next_step_handler(message, help)
#
#     elif message.text == "/history":
#         logger.info("Выполнение '/history'")
#         bot.register_next_step_handler(message, history)
#
#     elif message.text == "/start":
#         logger.info("Выполнение '/start'")
#         bot.register_next_step_handler(message, start)
#
#     elif message.text == "/hello-world" or message.text == "Привет":
#         bot.reply_to(message, "You are welcome!")
#         logger.info("Greetings")
#
#     else:
#         bot.reply_to(
#             message,
#             "Эхо без состояния или фильтра.\nСообщение: {message.text}",
#         )
#         logger.info("Empty echo")
