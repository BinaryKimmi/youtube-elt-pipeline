#fuctions related to database connections and operations


from airflow.providers.postgres.hooks.postgres import PostgresHook
#to interact with postgre database using python
from psycopg2.extras import RealDictCursor

#create the global table
table = "yt_api"

#setup connection and curcur objects
def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id = "postgres_db_yt_elt", database = "elt_db")
    conn = hook.get_conn()
    cur = conn.cursor(cursfor_factory=RealDictCursor)
    return conn, cur

#close cursor and connection
def close_conn_cur(conn, cur):
    cur.close()
    conn.close()

def create_schema(schema):
    conn, cur = get_conn_cursor()

    #create sql schema
    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    #run sql
    cur.execute(schema_sql)
    #commit changes to db
    conn.commit()

    close_conn_cur(conn, cur)

def create_table(schema):
    conn, cur = get_conn_cursor()

    #table names be the same for both schemas but different based on layer
    if schema == 'staging':
         table_sql = f"""
                 CREATE TABLE IF NOT EXISTS {schema}.{table} (
                     "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                     "Video_Title" TEXT NOT NULL,
                     "Upload_Date" TIMESTAMP NOT NULL,
                     "Duration" VARCHAR(20) NOT NULL,
                     "Video_Views" INT,
                     "Likes_Count" INT,
                     "Comments_Count" INT
                );
            """
                    
    else:
        table_sql = f"""
                 CREATE TABLE IF NOT EXISTS {schema}.{table} (
                     "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                     "Video_Title" TEXT NOT NULL,
                     "Upload_Date" TIMESTAMP NOT NULL,
                     "Duration" TIME NOT NULL,
                     "Video_Type" VARCHAR(10) NOT NULL,
                     "Video_Views" INT,
                     "Likes_Count" INT,
                     "Comments_Count" INT
                );
            """
    cur.execute(table_sql)

    conn.commit()

    close_conn_cur(conn, cur)    

         
#get all video ids
def get_video_ids(cur, schema):

    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table};""")
    ids = cur.fetchall()
    
 #going inside the video id field and extracting the value for each row 
    video_ids = [row['Video_ID'] for row in ids]
    return video_ids

       