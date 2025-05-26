import sys
import os
from prefect import flow, task
import pandas as pd

# Proje kök dizin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


from scripts.generate_simulation import generate_simulation_data
from database.insert_data import create_tables, insert_projects, insert_daily_progress



# Dosya pathleri
PROJECTS_CSV = os.path.join(BASE_DIR, "data", "raw", "projects.csv")
PROGRESS_CSV = os.path.join(BASE_DIR, "data", "processed", "daily_progress.csv")

# Veritabanı bağlantı parametreleri
DB_PARAMS = {
    "host": "localhost",
    "database": "construction",
    "user": "postgres",
    "password": "123456",
    "port": 5432,
}

@task
def generate_simulation_task():
    generate_simulation_data()
    print("✅ Simülasyon verisi oluşturuldu.")

@task
def load_data_task():
    import psycopg2
    conn = psycopg2.connect(**DB_PARAMS)

    create_tables(conn)

    df_projects = pd.read_csv(PROJECTS_CSV, parse_dates=["start_date"])
    df_progress = pd.read_csv(PROGRESS_CSV, parse_dates=["date"])

    insert_projects(conn, df_projects)
    insert_daily_progress(conn, df_progress)

    conn.close()
    print("✅ Veritabanına veri yüklendi.")

@flow(name="construction_etl_flow")
def construction_etl_flow():
    generate_simulation_task()
    load_data_task()

if __name__ == "__main__":
    construction_etl_flow()
