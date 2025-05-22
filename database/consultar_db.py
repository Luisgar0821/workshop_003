import sqlite3
import pandas as pd
import os

DB_PATH = "database/predictions.db"

# Verifica si la base de datos existe
if not os.path.exists(DB_PATH):
    print("No se encontró la base de datos. Asegúrate de que el consumidor la haya generado.")
    exit()

# Conectar a la base de datos
conn = sqlite3.connect(DB_PATH)

# Leer datos de la tabla
df = pd.read_sql_query("SELECT * FROM predictions", conn)

# Cerrar conexión
conn.close()

# Mostrar los primeros registros
print("Predicciones encontradas:")
print(df.head())

# Mostrar número de registros
print(f"\n Total de predicciones almacenadas: {len(df)}")

