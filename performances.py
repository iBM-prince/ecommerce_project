import time

def measure_query_time(cursor, query):
    """
    Mesure le temps d'exécution d'une requête SQL
    """
    start_time = time.time()
    cursor.execute(query)
    cursor.fetchall()
    end_time = time.time()
    return end_time - start_time
