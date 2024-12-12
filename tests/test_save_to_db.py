from unittest.mock import patch, MagicMock

from tomorrow.__main__ import save_to_db


@patch("tomorrow.__main__.get_db_connection")
@patch("tomorrow.__main__.is_record_present")
def test_save_to_db_success(mock_is_record_present, mock_get_db_connection):
    mock_is_record_present.return_value = False
    mock_conn = mock_get_db_connection.return_value.__enter__.return_value
    mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
    mock_cursor.execute = MagicMock()
    
    data = [{"lat": 25.8600, "lon": -97.4200, "temperature": 15, "windSpeed": 5, "time": "2024-12-12T00:00:00Z"}]
    result = save_to_db(data)
    assert result is True
    mock_cursor.execute.assert_called_once()

@patch("tomorrow.__main__.get_db_connection")
@patch("tomorrow.__main__.is_record_present")
def test_save_to_db_no_new_data(mock_is_record_present, mock_get_db_connection):
    mock_is_record_present.return_value = True  # Simulate duplicate data
    data = [{"lat": 25.8600, "lon": -97.4200, "temperature": 15, "windSpeed": 5, "time": "2024-12-12T00:00:00Z"}]
    result = save_to_db(data)
    assert result is False