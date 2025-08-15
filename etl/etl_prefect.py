import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
import subprocess

# Load .env (for local runs)
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "flight_delays")

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(db_url)

@task
def extract_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, low_memory=False)
    return df

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[
        "Year", "Month", "DayofMonth", "DayOfWeek",
        "Reporting_Airline", "Flight_Number_Reporting_Airline",
        "Origin", "Dest", 
        "CRSDepTime", "DepTime", "DepDelay", 
        "CRSArrTime", "ArrTime", "ArrDelay",
        "AirTime", "Distance"
    ]]

    df.columns = [
        "year", "month", "day", "day_of_week",
        "airline", "flight_number",
        "origin_airport", "destination_airport",
        "scheduled_departure", "departure_time", "departure_delay",
        "scheduled_arrival", "arrival_time", "arrival_delay",
        "air_time", "distance"
    ]

    df = df.dropna(subset=["flight_number", "origin_airport", "destination_airport"])

    time_cols = ["scheduled_departure", "departure_time", "scheduled_arrival", "arrival_time"]
    for col in time_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int).astype(str).str.zfill(4)

    int_cols = ["year", "month", "day", "day_of_week", "departure_delay", "arrival_delay", "air_time", "distance"]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    return df

@task
def load_to_postgres(df: pd.DataFrame):
    df.to_sql("flight_delays", engine, if_exists="append", index=False)

@task
def run_dbt():
    subprocess.run(["dbt", "run"], check=True, cwd="/Users/akshayin98/Desktop/flight_delay_pipeline/flight_delay_dbt")

@flow
def etl_flow(csv_path: str):
    raw_data = extract_data(csv_path)
    clean_data = transform_data(raw_data)
    load_to_postgres(clean_data)
    run_dbt()

if __name__ == "__main__":
    combined_csv_path = "/Users/akshayin98/Desktop/flight_delay_pipeline/data/raw/combined_flights_2024.csv"
    etl_flow(combined_csv_path)
