from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import re

app = FastAPI(title="Intent API", version="1.0.0")

API_KEY = os.getenv("API_KEY", "dev-key-123")
security = HTTPBearer()

# ---------- AUTH DEPENDENCY (FOR SWAGGER) ----------
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# ---------- ROOT (PUBLIC) ----------
@app.get("/")
def root():
    return {"status": "running"}


# ---------- INTENT ENDPOINT ----------
@app.post("/v1/intent-to-payload", dependencies=[Depends(verify_token)])
def intent_to_payload(body: dict):
    text = body.get("text", "")

    result = {
        "location": None,
        "inventoryType": None,
        "purpose": None,
        "budget": None,
        "startDate": None,
        "endDate": None,
    }

    # Location
    loc = re.search(r"in\s+([A-Za-z ]+)", text)
    if loc:
        result["location"] = loc.group(1).strip()

    # Inventory type
    if "billboard" in text.lower():
        result["inventoryType"] = "billboard"

    # Budget
    budget = re.search(r"\$([\d,]+)", text)
    if budget:
        result["budget"] = int(budget.group(1).replace(",", ""))

    # Purpose
    purpose = re.search(r"for\s+my\s+([A-Za-z ]+)", text)
    if purpose:
        result["purpose"] = purpose.group(1).strip()

    # Dates
    if "jan" in text.lower():
        result["startDate"] = "2026-01-01"
        result["endDate"] = "2026-01-31"

    missing = [k for k, v in result.items() if v is None]

    return {
        "parsed": result,
        "confidence": 0.95 if not missing else 0.6,
        "missingFields": missing,
        "warnings": []
    }
