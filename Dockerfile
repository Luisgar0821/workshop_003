FROM python:3.10

WORKDIR /app

# Instala las dependencias manualmente
RUN pip install pandas scikit-learn joblib kafka-python psycopg2-binary

COPY . .

CMD ["python", "kafka/consumer.py"]
