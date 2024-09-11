from datetime import datetime
from peewee import *
from loguru import logger

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username: str = CharField()  # Имя пользователя
    created_at: datetime = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )  # Время создания пользователя


class History(BaseModel):
    user: ForeignKeyField = ForeignKeyField(
        User
    )  # Внешний ключ на модель User
    date: datetime = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )  # Время записи
    content: str = TextField()  # Содержание записи


def initialize_database() -> None:
    """Создает подключение к базе данных и таблицы, если они не существуют."""
    db.connect()
    db.create_tables([User, History], safe=True)


initialize_database()
