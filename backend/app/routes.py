import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from fastapi import APIRouter, HTTPException
from app.schemas import DemandRequest, AnomalyRequest, SearchRequest, AgentRequest
from app.model_service import predict_demand, detect_anomaly
from app.data_service import get_dataset_summary, get_sales_overview
from app.database import (
    prediction_collection,
    agent_collection,
    document_collection
)
from app.logger import logger
from agents.agent_orchestrator import route_to_agent

router = APIRouter()

@router.get("/dataset-summary")
def dataset_summary():
    try:
        logger.info("Dataset summary API called")
        return get_dataset_summary()
    except Exception as e:
        logger.error(f"Dataset summary failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales-overview")
def sales_overview():
    try:
        logger.info("Sales overview API called")
        return get_sales_overview()
    except Exception as e:
        logger.error(f"Dataset summary failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict-demand")
def demand_prediction(request: DemandRequest):
    try:
        logger.info("Demand prediction API called")
        prediction = predict_demand(request.dict())
        prediction_collection.insert_one({
            "type": "demand_forecast",
            "input": request.dict(),
            "predicted_units_sold": prediction
})
        return {
            "predicted_units_sold": prediction,
            "message": "Demand forecast generated successfully"
        }
    except Exception as e:
        logger.error(f"Demand prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-anomaly")
def anomaly_prediction(request: AnomalyRequest):
    try:
        logger.info("Anomaly detection API called")
        result = detect_anomaly(request.dict())
        prediction_collection.insert_one({
           "type": "anomaly_detection",
           "input": request.dict(),
           "is_anomaly": result
})
        return {
            "is_anomaly": result,
            "message": "Anomaly detection completed"
        }
    except Exception as e:
        logger.error(f"Anomaly detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/document-search")
# def document_search(request: SearchRequest):
#     return {
#         "query": request.query,
#         "answer": "RAG document search will be connected in GenAI phase."
#     }


@router.post("/document-search")
def document_search(request: SearchRequest):

    try:
        logger.info("Document search API called")

        document_collection.insert_one({
            "query": request.query
        })

        return {
            "query": request.query,
            "answer": "RAG document search will be connected in GenAI phase."
        }

    except Exception as e:
        logger.error(f"Document search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



# @router.post("/agent-interaction")
# def agent_interaction(request: AgentRequest):

#     try:
#         logger.info("Agent interaction API called")

#         agent_collection.insert_one({
#             "question": request.question
#         })

#         return {
#             "question": request.question,
#             "agent_response": "Multi-agent system will answer using ML, analytics and document knowledge."
#         }

#     except Exception as e:
#         logger.error(f"Agent interaction failed: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent-interaction")
def agent_interaction(request: AgentRequest):

    try:
        logger.info("Agent interaction API called")

        agent_result = route_to_agent(request.question)

        try:
            agent_collection.insert_one({
                "question": request.question,
                "selected_agent": agent_result["selected_agent"],
                "response": str(agent_result["agent_response"])
            })
        except Exception as db_error:
            logger.error(f"MongoDB insert failed: {str(db_error)}")

        return {
            "question": request.question,
            "selected_agent": agent_result["selected_agent"],
            "agent_response": agent_result["agent_response"]
        }

    except Exception as e:
        logger.error(f"Agent interaction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))