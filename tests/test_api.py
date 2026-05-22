import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.append(
    str(Path(__file__).resolve().parents[1] / "backend")
)

from app.main import app
import app.routes as routes

client = TestClient(app)


class FakeCollection:
    def insert_one(self, data):
        return {"inserted_id": "test_id"}


routes.prediction_collection = FakeCollection()
routes.agent_collection = FakeCollection()
routes.document_collection = FakeCollection()


def test_home_api_status():
    response = client.get("/")
    assert response.status_code == 200


def test_home_api_message():
    response = client.get("/")
    assert "message" in response.json()


def test_dataset_summary_status():
    response = client.get("/dataset-summary")
    assert response.status_code == 200


def test_dataset_summary_rows():
    response = client.get("/dataset-summary")
    assert "rows" in response.json()


def test_dataset_summary_columns():
    response = client.get("/dataset-summary")
    assert "columns" in response.json()


def test_sales_overview_status():
    response = client.get("/sales-overview")
    assert response.status_code == 200


def test_sales_overview_revenue():
    response = client.get("/sales-overview")
    assert "total_revenue" in response.json()


def test_sales_overview_units():
    response = client.get("/sales-overview")
    assert "total_units_sold" in response.json()


def test_sales_overview_anomalies():
    response = client.get("/sales-overview")
    assert "total_anomalies" in response.json()


def test_predict_demand_valid_input():
    payload = {
        "discount_applied": 10,
        "clicks": 500,
        "impressions": 5000,
        "conversion_rate": 0.1,
        "ad_ctr": 0.08,
        "ad_cpc": 2.5,
        "ad_spend": 1200,
        "price_per_unit": 50,
        "year": 2025,
        "month": 6,
        "day": 15,
        "day_of_week": 2
    }

    response = client.post("/predict-demand", json=payload)
    assert response.status_code == 200
    assert "predicted_units_sold" in response.json()


def test_predict_demand_prediction_type():
    payload = {
        "discount_applied": 10,
        "clicks": 500,
        "impressions": 5000,
        "conversion_rate": 0.1,
        "ad_ctr": 0.08,
        "ad_cpc": 2.5,
        "ad_spend": 1200,
        "price_per_unit": 50,
        "year": 2025,
        "month": 6,
        "day": 15,
        "day_of_week": 2
    }

    response = client.post("/predict-demand", json=payload)
    assert isinstance(response.json()["predicted_units_sold"], (int, float))


def test_predict_demand_missing_field():
    response = client.post("/predict-demand", json={"clicks": 500})
    assert response.status_code == 422


def test_predict_demand_wrong_type():
    payload = {
        "discount_applied": "wrong",
        "clicks": 500,
        "impressions": 5000,
        "conversion_rate": 0.1,
        "ad_ctr": 0.08,
        "ad_cpc": 2.5,
        "ad_spend": 1200,
        "price_per_unit": 50,
        "year": 2025,
        "month": 6,
        "day": 15,
        "day_of_week": 2
    }

    response = client.post("/predict-demand", json=payload)
    assert response.status_code == 422


def test_predict_demand_high_campaign():
    payload = {
        "discount_applied": 40,
        "clicks": 5000,
        "impressions": 80000,
        "conversion_rate": 0.35,
        "ad_ctr": 0.20,
        "ad_cpc": 7.5,
        "ad_spend": 35000,
        "price_per_unit": 250,
        "year": 2025,
        "month": 11,
        "day": 27,
        "day_of_week": 5
    }

    response = client.post("/predict-demand", json=payload)
    assert response.status_code == 200


def test_detect_anomaly_valid_input():
    payload = {
        "units_sold": 100,
        "revenue": 5000,
        "conversion_rate": 0.1,
        "ad_spend": 1200,
        "clicks": 500,
        "impressions": 5000
    }

    response = client.post("/detect-anomaly", json=payload)
    assert response.status_code == 200
    assert "is_anomaly" in response.json()


def test_detect_anomaly_result_type():
    payload = {
        "units_sold": 100,
        "revenue": 5000,
        "conversion_rate": 0.1,
        "ad_spend": 1200,
        "clicks": 500,
        "impressions": 5000
    }

    response = client.post("/detect-anomaly", json=payload)
    assert isinstance(response.json()["is_anomaly"], bool)


def test_detect_anomaly_missing_field():
    response = client.post("/detect-anomaly", json={"units_sold": 100})
    assert response.status_code == 422


def test_detect_anomaly_wrong_type():
    payload = {
        "units_sold": "wrong",
        "revenue": 5000,
        "conversion_rate": 0.1,
        "ad_spend": 1200,
        "clicks": 500,
        "impressions": 5000
    }

    response = client.post("/detect-anomaly", json=payload)
    assert response.status_code == 422


def test_detect_anomaly_extreme_case():
    payload = {
        "units_sold": 9000,
        "revenue": 500000,
        "conversion_rate": 0.95,
        "ad_spend": 2,
        "clicks": 20,
        "impressions": 100
    }

    response = client.post("/detect-anomaly", json=payload)
    assert response.status_code == 200


def test_document_search_valid():
    response = client.post(
        "/document-search",
        json={"query": "What is the return policy?"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()


def test_document_search_has_query():
    response = client.post(
        "/document-search",
        json={"query": "What is the refund policy?"}
    )
    assert "query" in response.json()


def test_document_search_missing_query():
    response = client.post("/document-search", json={})
    assert response.status_code == 422


def test_agent_interaction_valid():
    response = client.post(
        "/agent-interaction",
        json={"question": "Which category has highest revenue?"}
    )
    assert response.status_code == 200
    assert "agent_response" in response.json()


def test_agent_interaction_has_question():
    response = client.post(
        "/agent-interaction",
        json={"question": "Which region has highest sales?"}
    )
    assert "question" in response.json()


def test_agent_interaction_missing_question():
    response = client.post("/agent-interaction", json={})
    assert response.status_code == 422


def test_invalid_get_route():
    response = client.get("/invalid-api")
    assert response.status_code == 404


def test_invalid_post_route():
    response = client.post("/invalid-api", json={})
    assert response.status_code == 404