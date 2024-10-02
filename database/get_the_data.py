from .data import History, User


def get_data(username):
    user = User.get(User.username == username)

    recent_history = (
        History.select()
        .where(History.user == user)
        .order_by(History.date.desc())
        .limit(10)
    )
    return recent_history
