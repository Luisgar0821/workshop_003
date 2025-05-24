from kafka import KafkaConsumer
import json
import joblib
import pandas as pd
import psycopg2
import sys
import os
from config_postgres import PG_CONFIG


# Cargar modelo y scaler
model = joblib.load("../models/happiness_model.pkl")
scaler = joblib.load("../models/scaler.pkl")

# Crear conexión inicial para asegurar tabla en PostgreSQL
conn = psycopg2.connect(**PG_CONFIG)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    gdp FLOAT,
    social_support FLOAT,
    health FLOAT,
    freedom FLOAT,
    trust FLOAT,
    generosity FLOAT,
    dystopia FLOAT,
    year INT,
    predicted_score FLOAT
)
""")
conn.commit()
cursor.close()
conn.close()

# Configurar Kafka
consumer = KafkaConsumer(
    'happiness_topic',
    bootstrap_servers='localhost:9092',  # nombre del servicio de kafka en Docker
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("📥 Esperando mensajes del topic...")

# Función para insertar en PostgreSQL
def insert_prediction_to_postgres(row, prediction):
    conn = psycopg2.connect(**PG_CONFIG)
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO predictions (
            gdp, social_support, health, freedom, trust,
            generosity, dystopia, year, predicted_score
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        row["GDP"],
        row["Social support"],
        row["Health"],
        row["Freedom"],
        row["Trust"],
        row["Generosity"],
        row["Dystopia"],
        row["Year"],
        prediction
    )
    cursor.execute(insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()

# Loop principal
for msg in consumer:
    data = msg.value
    df = pd.DataFrame([data])
    X = scaler.transform(df)
    predicted = float(model.predict(X)[0])

    insert_prediction_to_postgres(data, predicted)
    print(f"✅ Guardado en DB: Predicted Score = {predicted:.4f}")
