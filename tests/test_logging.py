from unittest.mock import patch
import requests

@patch("tomorrow.__main__.logger")
@patch("tomorrow.__main__.requests.get")
def test_logging(mock_requests_get, mock_logger):
    from tomorrow.__main__ import fetch_forecast

    # Simulate a RequestException being raised during the API call
    mock_requests_get.side_effect = requests.RequestException("API request failed")

    # Call the function to trigger the error
    fetch_forecast(25.8600, -97.4200)

    # Assert that logger.error was called
    mock_logger.error.assert_called_with("API request failed: API request failed")