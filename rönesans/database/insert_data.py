import psycopg2
import pandas as pd
import os

# Proje dizin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dosya paths
PROJECTS_CSV = os.path.join(BASE_DIR, "data", "raw", "projects.csv")
PROGRESS_CSV = os.path.join(BASE_DIR, "data", "processed", "daily_progress.csv")

# Veritabanı bağlantı
DB_PARAMS = {
    "host": "localhost",
    "database": "construction",
    "user": "postgres",
    "password": "123456",
    "port": 5432,
}

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY,
                project_name TEXT NOT NULL,
                city TEXT,
                country TEXT,
                category TEXT,
                start_date DATE,
                planned_duration_days INTEGER
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_progress (
                id SERIAL PRIMARY KEY,
                project_id INTEGER REFERENCES projects(project_id),
                date DATE NOT NULL,
                progress_percent NUMERIC(5,2),
                daily_cost BIGINT,
                number_of_workers INTEGER
            );
        """)
        conn.commit()
    print("✅ Tablolar oluşturuldu veya zaten mevcut.")

def insert_projects(conn, df_projects):
    with conn.cursor() as cur:
        for _, row in df_projects.iterrows():
            cur.execute("""
                INSERT INTO projects (project_id, project_name, city, country, category, start_date, planned_duration_days)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (project_id) DO NOTHING;
            """, (
                row['project_id'], row['project_name'], row['city'], row['country'], row['category'],
                row['start_date'], row['planned_duration_days']
            ))
        conn.commit()
    print("✅ Projects verileri yüklendi.")

def insert_daily_progress(conn, df_progress):
    with conn.cursor() as cur:
        for _, row in df_progress.iterrows():
            cur.execute("""
                INSERT INTO daily_progress (project_id, date, progress_percent, daily_cost, number_of_workers)
                VALUES (%s, %s, %s, %s, %s);
            """, (
                row['project_id'], row['date'], row['progress_percent'], row['daily_cost'], row['number_of_workers']
            ))
        conn.commit()
    print("✅ Daily progress verileri yüklendi.")

def main():
    print("PostgreSQL veritabanına bağlanılıyor...")
    conn = psycopg2.connect(**DB_PARAMS)

    create_tables(conn)

    print("CSV dosyaları okunuyor...")
    df_projects = pd.read_csv(PROJECTS_CSV, parse_dates=['start_date'])
    df_progress = pd.read_csv(PROGRESS_CSV, parse_dates=['date'])

    insert_projects(conn, df_projects)
    insert_daily_progress(conn, df_progress)

    conn.close()
    print("✅ Veri yükleme tamamlandı.")

if __name__ == "__main__":
    main()
