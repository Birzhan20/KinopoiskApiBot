from datetime import datetime
from loguru import logger
from database.data import User, History


def save_data(text: str, username: str) -> None:
    """Сохраняет данные о запросе пользователя в базе данных."""
    try:
        logger.info("Запись в базу")
        user, created = User.get_or_create(username=username)
        History.create(user=user, date=datetime.now(), content=text)
        logger.info("Запись успешно сохранена.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных: {e}")
