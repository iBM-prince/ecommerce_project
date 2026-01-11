import time
import mysql.connector
import pandas as pd

# Connexion à la base
def get_connection(user="root", password="", database="hopital_db"):
    return mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database
    )

# Exécution d'une requête SQL avec mesure du temps
def execute_query(query, user="root", password=""):
    conn = get_connection(user=user, password=password)
    cursor = conn.cursor(dictionary=True)

    start = time.time()
    cursor.execute(query)
    # Si SELECT, récupérer le résultat
    if query.strip().upper().startswith("SELECT"):
        result = cursor.fetchall()
        df = pd.DataFrame(result)
    else:
        conn.commit()  
        df = pd.DataFrame()
    end = time.time()

    cursor.close()
    conn.close()

    execution_time = end - start
    return df, execution_time
