import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kafka')))
from config_postgres import PG_CONFIG

def consultar_predicciones():
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 10;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    consultar_predicciones()
