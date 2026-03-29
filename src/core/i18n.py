import hashlib
import json
import os

USERS_DB_FILE = "users.json"
SALT = os.getenv("HASH_SALT", "fallback_salt")

supported_languages = ["it", "en"]
translations = {}

for lan in supported_languages:
    with open(f"lang/{lan}.json", "r", encoding="utf-8") as file:
        translations[lan] = json.load(file)


def _telegram_id_to_sha256(user_id: int) -> str:
    string_to_hash = f"{user_id}{SALT}"
    return hashlib.sha256(string_to_hash.encode("utf-8")).hexdigest()


def _load_users_db() -> dict:
    if not os.path.exists(USERS_DB_FILE):
        return {}
    try:
        with open(USERS_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def _save_users_db(data: dict):
    with open(USERS_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def set_user_language(user_id: int, lang: str = "en"):

    user_hash = _telegram_id_to_sha256(user_id)
    users = _load_users_db()

    users[user_hash] = lang

    _save_users_db(users)


def get_string(telegram_user, key: str) -> str:

    user_hash = _telegram_id_to_sha256(telegram_user.id)
    users = _load_users_db()

    lang = users.get(user_hash, "en")

    dictionary = translations.get(lang, translations["en"])

    return dictionary.get(key, key)
