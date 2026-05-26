import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client[DATABASE_NAME]

sales_collection = db["sales_records"]
prediction_collection = db["ml_predictions"]
agent_collection = db["agent_queries"]
document_collection = db["document_queries"]

print("MongoDB Atlas Connected Successfully")