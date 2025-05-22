from kafka import KafkaConsumer
import json
import joblib
import pandas as pd
import sqlite3  # Cambia si usarás otra base de datos
import os

# Cargar modelo y scaler
model = joblib.load("../models/happiness_model.pkl")
scaler = joblib.load("../models/scaler.pkl")

# Crear conexión a SQLite (base local)
conn = sqlite3.connect("../database/predictions.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    GDP REAL,
    SocialSupport REAL,
    Health REAL,
    Freedom REAL,
    Trust REAL,
    Generosity REAL,
    Dystopia REAL,
    Year INTEGER,
    PredictedScore REAL
)
""")
conn.commit()

# Crear consumidor
consumer = KafkaConsumer(
    'happiness_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("📥 Esperando mensajes del topic...")

# Escuchar y procesar
for msg in consumer:
    data = msg.value

    # Convertir a DataFrame para transformar con el scaler
    df = pd.DataFrame([data])
    X = scaler.transform(df)

    # Hacer predicción
    predicted = model.predict(X)[0]

    # Insertar en base de datos
    cursor.execute("""
        INSERT INTO predictions (GDP, SocialSupport, Health, Freedom, Trust, Generosity, Dystopia, Year, PredictedScore)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['GDP'],
        data['Social support'],
        data['Health'],
        data['Freedom'],
        data['Trust'],
        data['Generosity'],
        data['Dystopia'],
        data['Year'],
        predicted
    ))
    conn.commit()
    print(f"✅ Guardado en DB: Predicted Score = {predicted:.4f}")
