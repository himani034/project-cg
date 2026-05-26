import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

BASE_DIR = Path(__file__).resolve().parents[2]
env_path = BASE_DIR / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

DATA_DIR = BASE_DIR / "data"

RAW_FILE = DATA_DIR / "Smart Retail Assistant.csv"
STAGED_FILE = DATA_DIR / "cleaned_retail_sales_data.csv"
CURATED_CSV_FILE = DATA_DIR / "final_retail_ml_output.csv"
CURATED_PARQUET_FILE = DATA_DIR / "final_retail_ml_output.parquet"


def upload_to_blob(local_file_path, blob_path):
    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )

    container_client = blob_service_client.get_container_client(
        AZURE_STORAGE_CONTAINER
    )

    with open(local_file_path, "rb") as file:
        container_client.upload_blob(
            name=blob_path,
            data=file,
            overwrite=True
        )


def run_data_engineering_pipeline():
    df = pd.read_csv(RAW_FILE)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df = df.drop_duplicates()

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].fillna("Unknown")
        else:
            df[column] = df[column].fillna(0)

    df.to_csv(STAGED_FILE, index=False)

    curated_df = df.copy()

    if "revenue" in curated_df.columns and "units_sold" in curated_df.columns:
        curated_df["avg_price_per_unit"] = (
            curated_df["revenue"] / curated_df["units_sold"].replace(0, 1)
        )

    curated_df.to_csv(CURATED_CSV_FILE, index=False)
    curated_df.to_parquet(CURATED_PARQUET_FILE, index=False)

    upload_to_blob(RAW_FILE, "raw/Smart Retail Assistant.csv")
    upload_to_blob(STAGED_FILE, "staged/cleaned_retail_sales_data.csv")
    upload_to_blob(CURATED_CSV_FILE, "curated/final_retail_ml_output.csv")
    upload_to_blob(CURATED_PARQUET_FILE, "curated/final_retail_ml_output.parquet")

    return {
        "message": "Data engineering pipeline completed successfully",
        "flow": "Raw → Staged → Curated",
        "storage": "Azure Blob Storage",
        "parquet_created": True,
        "uploaded_files": [
            "raw/Smart Retail Assistant.csv",
            "staged/cleaned_retail_sales_data.csv",
            "curated/final_retail_ml_output.csv",
            "curated/final_retail_ml_output.parquet"
        ]
    }