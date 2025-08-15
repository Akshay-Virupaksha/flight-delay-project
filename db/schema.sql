CREATE TABLE IF NOT EXISTS flight_delays (
    id SERIAL PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    day_of_week INT,
    airline VARCHAR,
    flight_number VARCHAR,
    origin_airport VARCHAR,
    destination_airport VARCHAR,
    scheduled_departure INT,
    departure_time INT,
    departure_delay INT,
    scheduled_arrival INT,
    arrival_time INT,
    arrival_delay INT,
    air_time INT,
    distance INT
);

