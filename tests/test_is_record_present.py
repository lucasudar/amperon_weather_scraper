from unittest.mock import MagicMock
from tomorrow.__main__ import is_record_present


def test_is_record_present():
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = [True]
    result = is_record_present(mock_conn, -97.4200, 25.8600, "2024-12-12T00:00:00Z")
    assert result is True

def test_is_record_absent():
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = [False]
    result = is_record_present(mock_conn, -97.4200, 25.8600, "2024-12-12T00:00:00Z")
    assert result is False