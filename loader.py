from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from config_data import config


state_storage = StateMemoryStorage()


class UserStates(StatesGroup):
    waiting_for_from_year = State()
    waiting_for_to_year = State()
    waiting_for_country = State()


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=state_storage)
