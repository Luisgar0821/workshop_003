import sqlite3
import pandas as pd
import os

DB_PATH = "database/predictions.db"

if not os.path.exists(DB_PATH):
    print("No se encontró la base de datos. Asegúrate de que el consumidor la haya generado.")
    exit()

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM predictions", conn)

conn.close()

print("Predicciones encontradas:")
print(df.head())

print(f"\n Total de predicciones almacenadas: {len(df)}")

