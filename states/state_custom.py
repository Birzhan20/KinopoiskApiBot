from telebot.states import State, StatesGroup


class CustomGenreStates(StatesGroup):
    year_from = State()
    year_to = State()
    country = State()