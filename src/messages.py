from telegram import User

from src.core.i18n import get_string


def getAboutString(user: User) -> str:
    return get_string(user, "about_string")


def getServiceString(user: User) -> str:
    return get_string(user, "services_string")
