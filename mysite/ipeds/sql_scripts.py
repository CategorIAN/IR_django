import pyodbc, environ, os
from pathlib import Path
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent.parent

def queried_df(cursor, query):
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
    return pd.DataFrame(data=data, columns=columns)

def all_people():
    def execute(cursor):
        query = f"""
        SELECT ID,
         LAST_NAME,
         FIRST_NAME
         FROM PERSON
        """
        return queried_df(cursor, query)
    return execute

def readSQL(query):
    try:
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
        my_str = (
            f"DRIVER={{{env('DATABASE_DRIVER')}}};"
            f"SERVER={env('DATABASE_HOST')};"
            f"DATABASE={env('DATABASE_NAME')};"
            "Trusted_Connection=yes;"
        )
        connection = pyodbc.connect(my_str)
        cursor = connection.cursor()
        return queried_df(cursor, query)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
        print("MSSQL Connection Closed")