# ConstructionETL-Dashboard

# 🏗️ İnşaat Projeleri ETL ve Görselleştirme Dashboardu

Bu proje, inşaat projelerine ait verilerin simülasyonla üretilmesi, PostgreSQL veritabanına yüklenmesi ve Power BI ile görselleştirilmesini kapsayan bir veri mühendisliği ve analiz çözümüdür. Projede Prefect ile otomatikleştirilmiş ETL süreci uygulanmıştır.

## ⚙️ Kullanılan Teknolojiler

- **Python**
- **PostgreSQL**
- **Prefect (ETL otomasyonu)**
- **Power BI (Görselleştirme)**
- **Pandas** 
- **SQLAlchemy / psycopg2**

## 🚀 ETL Süreci

1. `generate_simulation_data()` fonksiyonu ile örnek proje ve günlük ilerleme verileri üretilir.
2. `create_tables()`, `insert_projects()`, `insert_daily_progress()` fonksiyonları ile veriler PostgreSQL veritabanına yüklenir.
3. Tüm bu işlemler, Prefect kullanılarak `construction_etl_flow` isimli bir akış içinde otomatikleştirilmiştir.

## 📊 Power BI Dashboard

Power BI üzerinde oluşturulan dashboard, aşağıdaki verileri sunmaktadır:

- 📈 Aylık bazda projelerin ilerleme yüzdesi
- 🏗️ Her proje için maksimum ilerleme
- 🕒 Proje zaman çizelgeleri
- 📍 Proje isimlerine göre genel ilerleme karşılaştırması





