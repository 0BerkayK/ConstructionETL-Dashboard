import pandas as pd
import random
import os
from datetime import datetime

def generate_simulation_data():

    # 1. Proje temel verileri (manuel veya web scrapping de yapılabilir)

    projects_data = [
        [1, "Allianz Tower", "İstanbul", "Türkiye", "Altyapı - Üstyapı"],
        [2, "Doğalgazdan Benzin Üretim Tesisi (GTG)", "Ahal", "Türkmenistan", "Endüstriyel İnşaatlar"],
        [3, "Premium CarPark P3", "Amsterdam", "Hollanda", "Altyapı - Üstyapı"],
        [4, "Nobo Otrobanda Hastanesi", "Willemstad", "Curacao", "Altyapı - Üstyapı"],
        [5, "St. Lucia Limanı Genişletme Projesi", "St. Lucia", "St. Lucia", "Altyapı - Üstyapı"],
        [6, "Gaziantep Şehir Hastanesi", "Gaziantep", "Türkiye", "Sağlık Yatırımı"],
        [7, "Başakşehir Çam ve Sakura Şehir Hastanesi", "İstanbul", "Türkiye", "Sağlık Yatırımı"],
        [8, "Adana Şehir Hastanesi", "Adana", "Türkiye", "Sağlık Yatırımı"],
        [9, "Bursa Şehir Hastanesi", "Bursa", "Türkiye", "Sağlık Yatırımı"],
        [10, "Elazığ Fethi Sekin Şehir Hastanesi", "Elazığ", "Türkiye", "Sağlık Yatırımı"],
        [11, "Yozgat Şehir Hastanesi", "Yozgat", "Türkiye", "Sağlık Yatırımı"],
        [12, "Talan Kuleleri", "Astana", "Kazakistan", "Üstyapı İnşaatlar"],
        [13, "Eleven Square", "Amsterdam", "Hollanda", "Üstyapı İnşaatlar"],
        [14, "Türkmenistan Bakanlık Binaları", "Aşkabat", "Türkmenistan", "Üstyapı İnşaatlar"],
        [15, "Nakkaş-Başakşehir Otoyolu Projesi", "İstanbul", "Türkiye", "Altyapı - Üstyapı"]
    ]

    start_dates = [
        "2021-12-01", "2022-01-15", "2022-03-10", "2022-04-25", "2022-05-20",
        "2022-06-15", "2022-07-10", "2022-08-05", "2022-09-01", "2022-10-10",
        "2022-11-05", "2022-12-20", "2023-01-15", "2023-02-25", "2023-03-30"
    ]
    start_dates = [pd.to_datetime(date) for date in start_dates]
    planned_durations = [450, 720, 300, 540, 360, 700, 720, 730, 600, 580, 560, 610, 420, 500, 390]

    projects_df = pd.DataFrame(projects_data, columns=["project_id", "project_name", "city", "country", "category"])
    projects_df["start_date"] = start_dates
    projects_df["planned_duration_days"] = planned_durations

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_path, 'data', 'raw', 'projects.csv')
    processed_path = os.path.join(base_path, 'data', 'processed', 'daily_progress.csv')

    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)

    projects_df.to_csv(raw_path, index=False)
    print("projects.csv oluşturuldu.")

    # ------------------------------
    # 2. Günlük ilerleme verilerini üretme (random)
    # ------------------------------
    progress_data = []

    for _, row in projects_df.iterrows():
        project_id = row["project_id"]
        start_date = row["start_date"]
        duration = row["planned_duration_days"]
        current_progress = 0.0

        for day in range(duration):
            date = start_date + pd.Timedelta(days=day)

            daily_progress = random.uniform(0.0005, 0.0025) * 100
            current_progress += daily_progress
            current_progress = min(current_progress, 100.0)

            daily_cost = random.randint(50000, 150000)
            daily_workers = random.randint(100, 500)

            progress_data.append([
                project_id, date.date(), round(current_progress, 2), daily_cost, daily_workers
            ])

            if current_progress >= 100.0:
                break

    progress_df = pd.DataFrame(progress_data, columns=[
        "project_id", "date", "progress_percent", "daily_cost", "number_of_workers"
    ])
    progress_df.to_csv(processed_path, index=False)
    print("daily_progress.csv oluşturuldu.")



if __name__ == "__main__":
    generate_simulation_data()
