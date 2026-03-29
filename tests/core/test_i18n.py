# pylint: disable=unused-argument

from unittest.mock import MagicMock, mock_open, patch

from src.core.i18n import (
    _load_users_db,
    _save_users_db,
    _telegram_id_to_sha256,
    get_string,
    set_user_language,
)


def test_telegram_id_to_sha256_is_deterministic():
    hash1 = _telegram_id_to_sha256(123456)
    hash2 = _telegram_id_to_sha256(123456)
    assert hash1 == hash2


def test_telegram_id_to_sha256_different_users():
    hash1 = _telegram_id_to_sha256(123456)
    hash2 = _telegram_id_to_sha256(789012)
    assert hash1 != hash2


@patch("os.path.exists", return_value=False)
def test_load_users_db_file_not_exists(mock_exists):
    result = _load_users_db()
    assert result == {}


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='{"user_hash_1": "it"}')
def test_load_users_db_valid_json(mock_file, mock_exists):
    # Se il file esiste ed è un JSON valido, deve restituire il dizionario
    result = _load_users_db()
    assert result == {"user_hash_1": "it"}


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="invalid_json")
def test_load_users_db_invalid_json(mock_file, mock_exists):
    # Se il JSON è corrotto, per evitare crash deve restituire un dizionario vuoto
    result = _load_users_db()
    assert result == {}


@patch("builtins.open", new_callable=mock_open)
@patch("src.core.i18n.json.dump")
def test_save_users_db(mock_json_dump, mock_file):
    # Verifica che la funzione provi a scrivere i dati nel file formattandoli correttamente
    dummy_data = {"user_hash_1": "en"}
    _save_users_db(dummy_data)

    mock_json_dump.assert_called_once_with(dummy_data, mock_file(), indent=4)


@patch("src.core.i18n._load_users_db", return_value={})
@patch("src.core.i18n._save_users_db")
def test_set_user_language_new_user(mock_save, mock_load):
    user_id = 12345
    set_user_language(user_id, "it")

    expected_hash = _telegram_id_to_sha256(user_id)
    mock_save.assert_called_once_with({expected_hash: "it"})


@patch("src.core.i18n._load_users_db")
@patch.dict(
    "src.core.i18n.translations", {"en": {"hello": "Hello"}, "it": {"hello": "Ciao"}}
)
def test_get_string_fallback_english(mock_load):
    # Se l'utente non è nel DB, deve usare l'inglese di default
    mock_load.return_value = {}

    mock_user = MagicMock()
    mock_user.id = 12345

    result = get_string(mock_user, "hello")
    assert result == "Hello"


@patch("src.core.i18n._load_users_db")
@patch.dict(
    "src.core.i18n.translations", {"en": {"hello": "Hello"}, "it": {"hello": "Ciao"}}
)
def test_get_string_with_saved_language(mock_load):
    mock_user = MagicMock()
    mock_user.id = 12345
    user_hash = _telegram_id_to_sha256(mock_user.id)

    mock_load.return_value = {user_hash: "it"}

    result = get_string(mock_user, "hello")
    assert result == "Ciao"


@patch("src.core.i18n._load_users_db", return_value={})
@patch.dict("src.core.i18n.translations", {"en": {}})
def test_get_string_missing_key(mock_load):
    # Se chiediamo una stringa che non esiste nel file JSON, deve restituire la chiave stessa come fallback
    mock_user = MagicMock()
    mock_user.id = 12345

    result = get_string(mock_user, "chiave_inesistente")
    assert result == "chiave_inesistente"
