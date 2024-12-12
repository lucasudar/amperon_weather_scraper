CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    geolocation GEOGRAPHY(POINT, 4326),
    temperature FLOAT CHECK (temperature BETWEEN -100 AND 100),
    wind_speed FLOAT CHECK (wind_speed >= 0),
    forecast_time TIMESTAMP,
    recorded_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_weather_data_geolocation ON weather_data USING GIST (geolocation);