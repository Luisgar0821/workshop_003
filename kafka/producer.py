from kafka import KafkaProducer
import pandas as pd
import json
import time

# Leer el dataset limpio (la ruta dentro del contenedor)
df = pd.read_csv("../data/happiness_cleaned.csv")

# Configurar Kafka para usar el hostname del contenedor (NO localhost)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # <- esto cambia para Docker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Enviar cada fila (menos "Country" y "Score")
for _, row in df.iterrows():
    data = row.drop(["Country", "Score"]).to_dict()
    producer.send("happiness_topic", value=data)
    print(f"✅ Enviado: {data}")
    time.sleep(5)  # espera simulada de envío

producer.flush()
