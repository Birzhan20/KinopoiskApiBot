from peewee import *
from telebot.types import Message
from loader import bot
from loguru import logger

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField()
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


class History(BaseModel):
    user = ForeignKeyField(User)
    date = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    content = TextField()


def initialize_database():
    db.connect()
    db.create_tables([User, History], safe=True)


initialize_database()


def save_data(message: Message):
    if message.text.startswith('/'):
        logger.info(f"Обрабатывается команда: {message.text}")
        try:
            user, created = User.get_or_create(username=message.from_user.username)
            History.create(
                user=user,
                content=message.text
            )
            logger.info("Запись успешно сохранена.")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных: {e}")
