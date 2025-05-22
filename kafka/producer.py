from kafka import KafkaProducer
import pandas as pd
import json
import time

df = pd.read_csv("data/happiness_cleaned.csv")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for _, row in df.iterrows():
    data = row.drop(["Country", "Score"]).to_dict()

    producer.send("happiness_topic", value=data)
    print(f"✅ Enviado: {data}")
    time.sleep(10)

producer.flush()
