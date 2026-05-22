import pickle
import pandas as pd
from pathlib import Path

# DEMAND_MODEL_PATH = Path("../ml_training/demand_forecasting_model.pkl")
# ANOMALY_MODEL_PATH = Path("../ml_training/anomaly_detection_model.pkl")

BASE_DIR = Path(__file__).resolve().parents[2]

DEMAND_MODEL_PATH = BASE_DIR / "ml_training" / "demand_forecasting_model.pkl"
ANOMALY_MODEL_PATH = BASE_DIR / "ml_training" / "anomaly_detection_model.pkl"


with open(DEMAND_MODEL_PATH, "rb") as file:
    demand_model = pickle.load(file)

with open(ANOMALY_MODEL_PATH, "rb") as file:
    anomaly_model = pickle.load(file)


def predict_demand(data):
    input_data = pd.DataFrame([data])
    prediction = demand_model.predict(input_data)[0]
    return round(float(prediction), 2)

def detect_anomaly(data):
    input_data = pd.DataFrame([data])
    prediction = anomaly_model.predict(input_data)[0]

    if prediction == -1:
        return True
    return False
