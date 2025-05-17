from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from backend.filters import filter_campaigns
from models.inference import generate_campaign_prediction

app = FastAPI()

# CORS settings (adjust origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for frontend filter submission
class FilterRequest(BaseModel):
    channel: Optional[List[str]] = None
    goal: Optional[str] = None
    audience: Optional[List[str]] = None
    segment: Optional[str] = None
    quarter: Optional[List[str]] = None
    location: Optional[List[str]] = None  

class CampaignInput(BaseModel):
    description: str

# API route to process filters and return campaign KPIs
@app.post("/filter-campaigns")
def get_filtered_campaigns(filters: FilterRequest):
    return filter_campaigns(
        channel=filters.channel,
        goal=filters.goal,
        audience=filters.audience,
        segment=filters.segment,
        quarter=filters.quarter,
        location=filters.location  
    )


@app.post("/predict-campaign-outcome")
def predict_campaign_outcome(payload: CampaignInput):
    result = generate_campaign_prediction(payload.description)
    return {"prediction": result}