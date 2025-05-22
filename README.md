# 🧠 Workshop 3: Machine Learning & Data Streaming – Happiness Score Prediction

This project implements a full Machine Learning pipeline combined with real-time data processing using Kafka. A regression model is trained to predict the Happiness Score of various countries using data from 2015 to 2019. A streaming system processes the data and stores predictions and features in a database.

---

## 📁 Project Structure

```
workshop_003/
│
├── data/                    # Cleaned CSV
│   └── dataset_limpio.csv
│
├── database/                # SQLite DB and query script
│   ├── predictions.db
│   └── consultar_db.py
│
├── kafka/                   # Kafka streaming scripts
│   ├── docker-compose.yml
│   ├── producer.py
│   └── consumer.py
│
├── models/                  # Trained model
│   ├── happiness_model.pkl
│   └── scaler.pkl
│
├── notebooks/
│   └── eda_etl.ipynb        # EDA and training
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

* Python
* Jupyter Notebook
* Pandas, Scikit-learn, Joblib
* Kafka + kafka-python
* SQLite
* Docker + Docker Compose

---

## 🔄 Project Flow

1. Load 5 CSV files with yearly happiness data.
2. Standardize and clean the data.
3. Train a regression model with 70-30 split.
4. Stream the cleaned dataset using Kafka (producer).
5. Consume the data, predict scores in real-time.
6. Store features and predictions in a database.

---

## 🧹 EDA and ETL

* Detected differences in columns between years.
* Renamed and standardized columns (`GDP`, `Health`, etc.).
* Dropped unnecessary columns (`Region`, `Standard Error`).
* Imputed missing values (`Trust`, `Dystopia`).

---

## 🧠 Model Training

* Model: `LinearRegression`
* Features used:

  * `GDP`, `Social support`, `Health`, `Freedom`, `Trust`, `Generosity`, `Dystopia`, `Year`
* Metrics:

  * 📈 **R² Score**: 0.9863
  * 📏 **RMSE**: 0.1307
  * 📉 **MSE**: 0.0171
  * 📊 **MAE**: 0.0990

---

## 🔁 Kafka Streaming

### Producer (`kafka/producer.py`)

* Reads from `dataset_limpio.csv`
* Sends each row to Kafka topic `happiness_topic` (excluding `Country` and `Score`)

### Consumer (`kafka/consumer.py`)

* Receives data from Kafka
* Applies `scaler.pkl`, predicts with `happiness_model.pkl`
* Inserts results into `predictions.db`

---

## 💾 SQLite Database

* Database: `predictions.db`
* Table: `predictions`
* Stores:

  * Input features
  * Year
  * Predicted `Happiness Score`

### Query results

Run:

```bash
python database/consultar_db.py
```

---

## 📊 Model Evaluation

Generated plot: Predicted vs Actual
Conclusion: The predictions closely follow the ideal line. No major error trends or outliers.

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone <repo-url>
cd workshop_003
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Kafka

```bash
cd kafka
docker-compose up -d
```

### 5. Run producer and consumer

In one terminal:

```bash
python kafka/consumer.py
```

In another terminal:

```bash
python kafka/producer.py
```

### 6. View predictions

```bash
python database/consultar_db.py
```

---

## 📦 Requirements (requirements.txt)

```txt
pandas
scikit-learn
joblib
kafka-python
```

---

## Project Status: **COMPLETE AND FUNCTIONAL**
