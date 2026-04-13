# Youtube API - ELT Pipeline

## 📌 Overview

This project builds a production-style ELT data pipeline using real YouTube channel data. 
Python scripts handle extraction via the YouTube API, 
data lands in a staged PostgreSQL database before being transformed and loaded into 
a core schema. The workflow is fully orchestrated with Apache Airflow, containerized 
using Docker, tested with pytest and SODA, and deployed automatically through 
GitHub Actions.

<img width="773" height="664" alt="image" src="https://github.com/user-attachments/assets/adb146af-569a-47b8-83e7-ce2a25e951e8" />

---

## 🏗️ Pipeline Architecture
 ```
YouTube API → Python Extraction → Staging Schema (PostgreSQL) → Transformation → Core Schema (PostgreSQL)
```


## 🔁 Pipeline DAG

DAG to produce JSON file with raw data
<img width="1050" height="379" alt="Screenshot 2026-04-05 at 10 29 05 AM" src="https://github.com/user-attachments/assets/9ecb24e0-4559-49ec-a34f-4725ea226d97" />

DAG to process JSON file and insert data into both staging and core schemas
<img width="712" height="145" alt="Screenshot 2026-04-13 at 12 51 01 AM" src="https://github.com/user-attachments/assets/f5406d3e-fd6a-4a79-81e6-5f631c72d5cf" />

DAG to check the data quality on both layers in the database

<img width="500" height="145" alt="Screenshot 2026-04-13 at 12 54 10 AM" src="https://github.com/user-attachments/assets/08ac5f6b-4274-4373-8a48-49c11231ad8f" />



## 🛠️ Tools & Technologies

| Category | Tool |
|---|---|
| Containerization | Docker, Docker Compose |
| Orchestration | Apache Airflow |
| Data Storage | PostgreSQL |
| Languages | Python, SQL |
| Testing | pytest, SODA |
| CI/CD | GitHub Actions |




