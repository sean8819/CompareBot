from unittest.mock import MagicMock, patch

from telegram import User

from src.messages import getAboutString, getServiceString


@patch("src.messages.get_string")
def test_getAboutString(mock_get_string):
    mock_user = MagicMock(spec=User)
    mock_get_string.return_value = "Testo About"

    result = getAboutString(mock_user)

    mock_get_string.assert_called_once_with(mock_user, "about_string")
    assert result == "Testo About"


@patch("src.messages.get_string")
def test_getServiceString(mock_get_string):
    mock_user = MagicMock(spec=User)
    mock_get_string.return_value = "Testo Servizi"

    result = getServiceString(mock_user)

    mock_get_string.assert_called_once_with(mock_user, "services_string")
    assert result == "Testo Servizi"
