import time
import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # ⚠️ mets ton mot de passe MySQL si besoin
        database="hopital_db"
    )

def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    start = time.time()
    cursor.execute(query)
    result = cursor.fetchall()
    end = time.time()

    cursor.close()
    conn.close()

    execution_time = end - start
    return pd.DataFrame(result), execution_time
