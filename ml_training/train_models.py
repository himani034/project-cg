# import pandas as pd
# import pickle
# from pathlib import Path

# from sklearn.model_selection import train_test_split
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.pipeline import Pipeline
# from sklearn.ensemble import RandomForestRegressor, IsolationForest
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# DATA_PATH = Path("../data/cleaned_retail_sales_data.csv")

# DEMAND_MODEL_PATH = Path("demand_forecasting_model.pkl")
# ANOMALY_MODEL_PATH = Path("anomaly_detection_model.pkl")

# df = pd.read_csv(DATA_PATH)
# df = df.dropna()

# df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
# df["year"] = df["transaction_date"].dt.year
# df["month"] = df["transaction_date"].dt.month
# df["day"] = df["transaction_date"].dt.day
# df["day_of_week"] = df["transaction_date"].dt.dayofweek

# df["price_per_unit"] = df["revenue"] / df["units_sold"].replace(0, 1)
# df["price_per_unit"] = df["price_per_unit"].fillna(0)

# df = df.dropna()

# numeric_features = [
#     "discount_applied",
#     "clicks",
#     "impressions",
#     "conversion_rate",
#     "ad_ctr",
#     "ad_cpc",
#     "ad_spend",
#     "price_per_unit",
#     "year",
#     "month",
#     "day",
#     "day_of_week"
# ]

# categorical_features = [
#     "category",
#     "region"
# ]

# features = numeric_features + categorical_features
# target = "units_sold"

# X = df[features]
# y = df[target]

# X_train, X_test, y_train, y_test = train_test_split(
#     X,
#     y,
#     test_size=0.2,
#     random_state=42
# )

# preprocessor = ColumnTransformer(
#     transformers=[
#         ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
#     ],
#     remainder="passthrough"
# )

# demand_model = Pipeline(steps=[
#     ("preprocessor", preprocessor),
#     ("model", RandomForestRegressor(
#         n_estimators=400,
#         max_depth=22,
#         min_samples_split=3,
#         min_samples_leaf=1,
#         random_state=42,
#         n_jobs=-1

        
#     ))
# ])

# demand_model.fit(X_train, y_train)

# predictions = demand_model.predict(X_test)

# mae = mean_absolute_error(y_test, predictions)
# rmse = mean_squared_error(y_test, predictions) ** 0.5
# r2 = r2_score(y_test, predictions)
# approx_accuracy = max(0, r2 * 100)

# print("\nDemand Forecasting Model")
# print("MAE:", round(mae, 2))
# print("RMSE:", round(rmse, 2))
# print("R2 Score:", round(r2, 2))
# print("Approx Accuracy:", round(approx_accuracy, 2), "%")

# with open(DEMAND_MODEL_PATH, "wb") as file:
#     pickle.dump(demand_model, file)

# print("Demand model saved successfully")

# anomaly_features = [
#     "units_sold",
#     "revenue",
#     "conversion_rate",
#     "ad_spend",
#     "clicks",
#     "impressions"
# ]

# anomaly_data = df[anomaly_features]

# anomaly_model = IsolationForest(
#     contamination=0.05,
#     random_state=42
# )

# anomaly_model.fit(anomaly_data)

# df["model_anomaly_prediction"] = anomaly_model.predict(anomaly_data)
# df["model_anomaly_prediction"] = df["model_anomaly_prediction"].map({
#     1: 0,
#     -1: 1
# })

# with open(ANOMALY_MODEL_PATH, "wb") as file:
#     pickle.dump(anomaly_model, file)

# df.to_csv("../data/final_retail_ml_output.csv", index=False)

# print("\nAnomaly Detection Model")
# print("Anomaly model saved successfully")
# print("Final ML output saved at data/final_retail_ml_output.csv")




import pandas as pd
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path("../data/cleaned_retail_sales_data.csv")

DEMAND_MODEL_PATH = Path("demand_forecasting_model.pkl")
ANOMALY_MODEL_PATH = Path("anomaly_detection_model.pkl")

df = pd.read_csv(DATA_PATH)
df = df.dropna()

df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

df["year"] = df["transaction_date"].dt.year
df["month"] = df["transaction_date"].dt.month
df["day"] = df["transaction_date"].dt.day
df["day_of_week"] = df["transaction_date"].dt.dayofweek

df["price_per_unit"] = df["revenue"] / df["units_sold"].replace(0, 1)
df["price_per_unit"] = df["price_per_unit"].fillna(0)

df = df.dropna()

numeric_features = [
    "discount_applied",
    "clicks",
    "impressions",
    "conversion_rate",
    "ad_ctr",
    "ad_cpc",
    "ad_spend",
    "price_per_unit",
    "year",
    "month",
    "day",
    "day_of_week"
]

categorical_features = [
    "category",
    "region"
]

features = numeric_features + categorical_features
target = "units_sold"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

demand_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=50,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1
    ))
])

demand_model.fit(X_train, y_train)

predictions = demand_model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)
approx_accuracy = max(0, r2 * 100)

print("\nDemand Forecasting Model")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 2))
print("Approx Accuracy:", round(approx_accuracy, 2), "%")

with open(DEMAND_MODEL_PATH, "wb") as file:
    pickle.dump(demand_model, file)

print("Demand model saved successfully")

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
    -1: 1
})

with open(ANOMALY_MODEL_PATH, "wb") as file:
    pickle.dump(anomaly_model, file)

df.to_csv("../data/final_retail_ml_output.csv", index=False)

print("\nAnomaly Detection Model")
print("Anomaly model saved successfully")
print("Final ML output saved at data/final_retail_ml_output.csv")