import pandas as pd
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

DATA_PATH = Path("../data/cleaned_retail_sales_data.csv")

DEMAND_MODEL_PATH = Path("demand_forecasting_model.pkl")
ANOMALY_MODEL_PATH = Path("anomaly_detection_model.pkl")


df = pd.read_csv(DATA_PATH)

# Demand Forecasting model
features = [
    "discount_applied",
    "clicks",
    "impressions",
    "conversion_rate",
    "ad_ctr",
    "ad_cpc",
    "ad_spend",
    "price_per_unit",
    # "revenue",
    "year",
    "month",
    "day",
    "day_of_week"
]

target = "units_sold"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

demand_model = RandomForestRegressor(
    n_estimators=150,
    max_depth=12,
    random_state=42
)

demand_model.fit(X_train, y_train)

predictions = demand_model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nDemand Forecasting Model")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 2))

with open(DEMAND_MODEL_PATH, "wb") as file:
    pickle.dump(demand_model, file)

print("Demand model saved successfully")

print("\nDemand Forecasting Model")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 2))

# with open(DEMAND_MODEL_PATH, "wb") as file:
#     pickle.dump(demand_model, file)

# print("Demand model saved successfully")

# Anomaly Detection model
anomaly_features = [
    "units_sold",
    "revenue",
    "conversion_rate",
    "ad_spend",
    "clicks",
    "impressions"
]

anomaly_data = df[anomaly_features]

anomaly_model = IsolationForest(
    contamination=0.05,
    random_state=42
)

anomaly_model.fit(anomaly_data)

df["model_anomaly_prediction"] = anomaly_model.predict(anomaly_data)

df["model_anomaly_prediction"] = df["model_anomaly_prediction"].map({
    1: 0,
    -1 : 1
})

with open(ANOMALY_MODEL_PATH, "wb") as file:
    pickle.dump(anomaly_model, file)

df.to_csv("../data/final_retail_ml_output.csv", index=False)

print("\nAnomaly Detection Model")
print("Anomaly model saved successfully")
print("Final ML output saved at data/final_retail_ml_output.csv")