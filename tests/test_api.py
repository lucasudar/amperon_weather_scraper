from unittest.mock import patch
from tomorrow.__main__ import fetch_forecast


@patch("requests.get")
def test_fetch_forecast_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": {
            "timelines": [{
                "intervals": [
                    {"startTime": "2024-12-12T00:00:00Z",
                        "values": {"temperature": 15, "windSpeed": 5}}
                ]
            }]
        }
    }
    result = fetch_forecast(25.8600, -97.4200)
    assert len(result) == 1
    assert result[0]["temperature"] == 15
    assert result[0]["windSpeed"] == 5
