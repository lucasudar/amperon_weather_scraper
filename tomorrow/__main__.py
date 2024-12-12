import requests
import psycopg2
from datetime import datetime, timedelta, timezone
import logging
import time
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")

LOCATIONS = [
    (25.8600, -97.4200), (25.9000, -97.5200), (25.9000, -97.4800),
    (25.9000, -97.4400), (25.9000, -97.4000), (25.9200, -97.3800),
    (25.9400, -97.5400), (25.9400, -97.5200), (25.9400, -97.4800), (25.9400, -97.4400)
]


def fetch_forecast(lat, lon):
    """
    Fetch weather forecast for given coordinates.

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        list: Extracted weather forecast data
    """
    url = "https://api.tomorrow.io/v4/timelines"

    # Use a fixed time range instead of dynamically generated
    start_time = datetime.now(timezone.utc).replace(
        minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=5)

    params = {
        "apikey": API_KEY,
        "location": f"{lat},{lon}",
        "fields": ["temperature", "windSpeed"],
        "timesteps": "1h",
        "startTime": start_time.isoformat(),
        "endTime": end_time.isoformat()
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract data for each time entry
        extracted = []
        for interval in data['data']['timelines'][0]['intervals']:
            extracted.append({
                "lat": lat,
                "lon": lon,
                "temperature": interval['values']['temperature'],
                "windSpeed": interval['values']['windSpeed'],
                "time": interval['startTime']
            })

        return extracted

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return []


def get_db_connection():
    """
    Establish and return a database connection with retry mechanism.

    Returns:
        psycopg2.connection: Database connection
    """
    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname="tomorrow", user="postgres", password="postgres", host="postgres"
            )
            return conn

        except psycopg2.OperationalError as e:
            # Fixed the f-string by completing the formatting
            logger.warning("Retry %s doesn't happen: %s", attempt + 1, str(e))
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                logger.error(
                    "Failed to connect to database after multiple attempts")
                raise


def is_record_present(conn, lon, lat, time):
    """
    Check if a record already exists in the database.

    Args:
        conn (psycopg2.connection): Database connection
        lon (float): Longitude
        lat (float): Latitude
        time (str): Forecast time

    Returns:
        bool: True if record exists, False otherwise
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1 FROM weather_data 
                WHERE geolocation = ST_Point(%s, %s) AND forecast_time = %s
            )
            """,
            (lon, lat, time)
        )
        return cursor.fetchone()[0]


def save_to_db(data):
    """
    Save weather forecast data to database.

    Args:
        data (list): Weather forecast data

    Returns:
        bool: True if save was successful, False otherwise
    """
    if not data:
        logger.warning("No data to save")
        return False

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                new_records_count = 0
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
                        new_records_count += 1

                conn.commit()
                logger.info(f"Saved {new_records_count} new records")
                return new_records_count > 0

    except Exception as e:
        logger.error(f"Database save failed: {e}")
        return False


def main():
    """
    Main function to fetch and save weather forecast data.
    """
    if not API_KEY:
        logger.error("API key is not set. Please provide TOMORROW_IO_API_KEY.")
        return

    for lat, lon in LOCATIONS:
        try:
            forecast_data = fetch_forecast(lat, lon)
            saved = save_to_db(forecast_data)

            if saved:
                logger.info(f"Successfully processed location ({lat}, {lon})")
            else:
                logger.info(f"No new data for location ({lat}, {lon})")

        except Exception as e:
            logger.error(f"Error processing location ({lat}, {lon}): {e}")

        # Small delay between location processing
        time.sleep(10)

    # Final log after processing all locations
    logger.info("All locations processed successfully.")


if __name__ == "__main__":
    main()
