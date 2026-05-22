import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("../data/Smart Retail Assistant.csv")
CLEAN_DATA_PATH = Path("../data/cleaned_retail_sales_data.csv")

def clean_retail_dataset():
    df = pd.read_csv(RAW_DATA_PATH)

    print("Original Shape: ", df.shape)
    print("Original Columns: ", list(df.columns))

    # cleaning column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # removing duplicate transactions
    df = df.drop_duplicates()

    # convert date column
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    # remove rows with invalid date
    df = df.dropna(subset=["transaction_date"])

    # fill missing values
    text_columns = ["transaction_id", "customer_id", "product_id", "category", "region"]
    number_columns = [
        "units_sold",
        "discount_applied",
        "revenue",
        "clicks",
        "impressions",
        "conversion_rate",
        "ad_ctr",
        "ad_cpc",
        "ad_spend"
    ]
    
    for col in text_columns:
        df[col] = df[col].fillna("Unknown")
    for col in number_columns:
        df[col] = df[col].fillna(df[col].median())

    # remove invalid negative values
    for col in number_columns:
        df = df[df[col] >= 0]

    # Feature Engineering
    df["year"] = df["transaction_date"].dt.year
    df["month"] = df["transaction_date"].dt.month
    df["day"] = df["transaction_date"].dt.day
    df["day_of_week"] = df["transaction_date"].dt.dayofweek

    # create price per unit
    df["price_per_unit"] = df["revenue"] / df["units_sold"]
    df["price_per_unit"] = df["price_per_unit"].replace([float("inf")], 0)
    df["price_per_unit"] = df["price_per_unit"].fillna(0)

    # creating anomaly flag
    revenue_limit = df["revenue"].quantile(0.99)
    low_conversion_limit = df["conversion_rate"].quantile(0.01)

    df["is_anomaly"] = 0
    df.loc[df["revenue"] > revenue_limit, "is_anomaly"] = 1
    df.loc[df["conversion_rate"] < low_conversion_limit, "is_anomaly"] = 1
    df.loc[df["units_sold"] == 0, "is_anomaly"] = 1

    df.to_csv(CLEAN_DATA_PATH, index=False)

    print("Cleaned shape:", df.shape)
    print("Cleaned columns:", list(df.columns))
    print("Cleaned dataset saved at:", CLEAN_DATA_PATH)


if __name__ == "__main__":
    clean_retail_dataset()