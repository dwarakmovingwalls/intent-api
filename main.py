import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="Intent Translation API",
    version="1.0.0"
)

API_KEY = os.getenv("API_KEY")

class IntentRequest(BaseModel):
    text: str

class IntentResponse(BaseModel):
    parsed: dict
    confidence: float
    missingFields: List[str]
    warnings: List[str]

@app.post("/v1/intent-to-payload", response_model=IntentResponse)
def parse_intent(
    request: IntentRequest,
    authorization: Optional[str] = Header(None)
):
    if not API_KEY or authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Temporary hardcoded response (replace later with LLM logic)
    return {
        "parsed": {
            "location": "California",
            "inventoryType": "billboard",
            "purpose": "coffee shop",
            "budget": 5000,
            "startDate": "2026-01-01",
            "endDate": "2026-01-31"
        },
        "confidence": 0.95,
        "missingFields": [],
        "warnings": []
    }

