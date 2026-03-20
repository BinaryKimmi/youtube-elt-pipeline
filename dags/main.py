from airflow import DAG
import pendulum #deals with timezones
from datetime import datetime, timedelta
from api.video_stats import (
    get_playlist_id, 
    get_video_ids, 
    extract_video_data, 
    save_to_json,
)

from datawarehouse.dwh import staging_table, core_table

#Define the local timezone
local_tz = pendulum.timezone("America/Jamaica")

#Default Args
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": ["dataengineers.com"],
    #"retries": 1,
    #"retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 1, 1, tzinfo=local_tz),
    # "end_date": datetime(2030, 12, 31, tzinfo=local_tz),
}

#Create a DAG
with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='DAG to output json file with raw data',
    schedule='0 14 * * *',
    catchup=False
) as dag:
    #define tasks by calling functions in video_stats.py
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    #Define dependencies (what order should the task run from left to right)
    playlist_id >> video_ids >> extract_data >> save_to_json_task


with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='DAG to process JSON file and insert data into both staging and core schemas',
    schedule='0 15 * * *',
    catchup=False
) as dag:
    #define tasks by calling functions in video_stats.py
    update_staging = staging_table()
    update_core = core_table()
    
    #Define dependencies (what order should the task run from left to right)
    update_staging >> update_core 

