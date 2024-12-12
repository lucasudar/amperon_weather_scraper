import requests
import psycopg2
from datetime import datetime, timedelta, timezone
import logging
import time


# configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

logging.info("WELCOME!")

API_KEY = "h2xGnZitLX3EpkvSrJLcKQq9qXNvQY75"
# LOCATIONS = [
#     (25.8600, -97.4200), (25.9000, -97.5200), (25.9000, -97.4800),
#     (25.9000, -97.4400), (25.9000, -97.4000), (25.9200, -97.3800),
#     (25.9400, -97.5400), (25.9400, -97.5200), (25.9400, -97.4800), (25.9400, -97.4400)
# ]

LOCATIONS = [(25.8600, -97.4200)]


def fetch_forecast(lat, lon):
    url = "https://api.tomorrow.io/v4/timelines"
    start_time = datetime.now(timezone.utc).isoformat()
    end_time = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    params = {
        "apikey": API_KEY,
        "location": f"{lat},{lon}",
        "fields": ["temperature", "windSpeed"],
        "timesteps": "1h",
        "startTime": start_time,
        "endTime": end_time
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    # Extract data for each time entry
    extracted = []
    for interval in data['data']['timelines'][0]['intervals']:
        print(interval)
        extracted.append({
            "lat": lat,
            "lon": lon,
            "temperature": interval['values']['temperature'],
            "windSpeed": interval['values']['windSpeed'],
            "time": interval['startTime']
        })
    return extracted


def is_record_present(conn, lon, lat, time):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM weather_data 
            WHERE geolocation = ST_Point(%s, %s) AND forecast_time = %s
        )
        """,
        (lon, lat, time)
    )
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def save_to_db(data):
    try:
        conn = psycopg2.connect(
            dbname="tomorrow", user="postgres", password="postgres", host="postgres"
        )
        cursor = conn.cursor()
        for record in data:
            if not is_record_present(conn, record['lon'], record['lat'], record['time']):
                cursor.execute(
                    """
                    INSERT INTO weather_data (geolocation, temperature, wind_speed, forecast_time)
                    VALUES (ST_Point(%s, %s), %s, %s, %s)
                    """,
                    (record['lon'], record['lat'], record['temperature'],
                     record['windSpeed'], record['time'])
                )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"Database not ready, retrying: {e}")
        time.sleep(5)  # Wait 5 seconds before retrying


if __name__ == "__main__":
    for lat, lon in LOCATIONS:
        try:
            forecast_data = fetch_forecast(lat, lon)
            save_to_db(forecast_data)
            logging.info(
                f"Successfully saved data for location ({lat}, {lon})")
        except Exception as e:
            print(f"Error processing location ({lat}, {lon}): {e}")
        finally:
            time.sleep(2)
