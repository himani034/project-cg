import pandas as pd

df = pd.read_parquet("data/final_retail_ml_output.parquet")

print(df.head())