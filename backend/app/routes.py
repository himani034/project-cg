import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from fastapi import APIRouter, HTTPException

from app.schemas import (
    DemandRequest,
    AnomalyRequest,
    SearchRequest,
    AgentRequest,
    DocumentIntelligenceRequest,
    TextAnalyticsRequest
)

from app.model_service import predict_demand, detect_anomaly
from app.data_service import get_dataset_summary, get_sales_overview

from app.database import (
    prediction_collection,
    agent_collection,
    document_collection
)

from app.logger import logger
from agents.agent_orchestrator import route_to_agent

from rag.document_loader import load_documents

from app.azure_search_service import (
    create_search_index,
    upload_documents_to_search,
    search_azure_documents
)

from app.document_intelligence_service import extract_text_from_pdf_url
from app.text_analytics_service import analyze_customer_text

from app.data_pipeline_service import run_data_engineering_pipeline

# router = APIRouter()
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


# from datetime import datetime

@router.post("/agent-interaction")
def agent_interaction(request: AgentRequest):
    logger.info("Agent interaction API called")

    try:
        agent_result = route_to_agent(request.question)

        if isinstance(agent_result["agent_response"], dict):
            answer_text = agent_result["agent_response"].get("answer")
        else:
            answer_text = str(agent_result["agent_response"])

        insert_result = agent_collection.insert_one({
            "question": request.question,
            "selected_agent": agent_result["selected_agent"],
            "answer": answer_text,
            "full_response": agent_result["agent_response"],
            "created_at": datetime.utcnow(),
            "status": "answered"
        })

        print("Inserted ID:", insert_result.inserted_id)

        return {
            "question": request.question,
            "selected_agent": agent_result["selected_agent"],
            "agent_response": agent_result["agent_response"]
        }

    except Exception as e:
        print("Agent interaction failed:", e)
        logger.error(f"Agent interaction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/azure-search/create-index")
def create_azure_search_index():
    try:
        return create_search_index()
    except Exception as e:
        logger.error(f"Azure Search index creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/azure-search/upload-documents")
def upload_azure_search_documents():
    try:
        documents = load_documents()
        return upload_documents_to_search(documents)
    except Exception as e:
        logger.error(f"Azure Search upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/azure-search/search")
def azure_search(query: str):
    try:
        results = search_azure_documents(query)
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        logger.error(f"Azure Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/document-intelligence")
def document_intelligence(request: DocumentIntelligenceRequest):
    try:
        result = extract_text_from_pdf_url(request.pdf_url)

        return {
            "pdf_url": request.pdf_url,
            "extracted_result": result,
            "message": "Azure Document Intelligence completed successfully"
        }

    except Exception as e:
        logger.error(f"Document Intelligence failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/text-analytics")
def text_analytics(request: TextAnalyticsRequest):
    try:
        result = analyze_customer_text(request.text)

        return {
            "text": request.text,
            "analysis": result,
            "message": "Azure Text Analytics completed successfully"
        }

    except Exception as e:
        logger.error(f"Text Analytics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/data-pipeline/run")
def run_pipeline():
    try:
        return run_data_engineering_pipeline()
    except Exception as e:
        logger.error(f"Data pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))