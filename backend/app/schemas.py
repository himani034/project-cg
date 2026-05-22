from pydantic import BaseModel

class DemandRequest(BaseModel):
    discount_applied: float
    clicks: int
    impressions: int
    conversion_rate: float
    ad_ctr: float
    ad_cpc: float
    ad_spend: float
    price_per_unit: float
    # revenue: float
    year: int
    month: int
    day: int
    day_of_week: int


class AnomalyRequest(BaseModel):
    units_sold: int
    revenue: float
    conversion_rate: float
    ad_spend: float
    clicks: int
    impressions: int

class SearchRequest(BaseModel):
    query: str


class AgentRequest(BaseModel):
    question: str