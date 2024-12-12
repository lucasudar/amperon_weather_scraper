from unittest.mock import patch


@patch("tomorrow.__main__.time.sleep")
@patch("tomorrow.__main__.save_to_db")
@patch("tomorrow.__main__.fetch_forecast")
def test_main(mock_fetch_forecast, mock_save_to_db, mock_sleep):
    from tomorrow.__main__ import main
    mock_fetch_forecast.return_value = [
        {"lat": 25.8600, "lon": -97.4200, "temperature": 15,
            "windSpeed": 5, "time": "2024-12-12T00:00:00Z"}
    ]
    mock_save_to_db.return_value = True
    mock_sleep.return_value = None  # Mocking time.sleep to skip the delay
    main()
    mock_fetch_forecast.assert_called()
    mock_save_to_db.assert_called()
