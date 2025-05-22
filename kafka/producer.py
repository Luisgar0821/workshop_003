from kafka import KafkaProducer
import pandas as pd
import json
import time

# Cargar el dataset limpio
df = pd.read_csv("../data/happiness_cleaned.csv")

# Crear el productor Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Enviar cada fila del DataFrame
for _, row in df.iterrows():
    # Excluir columnas que no se usaron para entrenar el modelo
    data = row.drop(["Country", "Score"]).to_dict()
    
    # Enviar al topic
    producer.send("happiness_topic", value=data)
    print(f"✅ Enviado: {data}")
    time.sleep(10)

producer.flush()
