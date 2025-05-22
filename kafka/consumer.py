from kafka import KafkaConsumer
import json
import joblib
import pandas as pd
import sqlite3  
import os

model = joblib.load("models/happiness_model.pkl")
scaler = joblib.load("models/scaler.pkl")

conn = sqlite3.connect("database/predictions.db")
cursor = conn.cursor()

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

consumer = KafkaConsumer(
    'happiness_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("📥 Esperando mensajes del topic...")

for msg in consumer:
    data = msg.value

    df = pd.DataFrame([data])
    X = scaler.transform(df)

    predicted = model.predict(X)[0]

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
