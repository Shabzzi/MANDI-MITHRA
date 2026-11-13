"""Optional AGMARKNET/data.gov.in connector for MandiMitra AI.
Run: uvicorn main:app --host 127.0.0.1 --port 8001
"""
from __future__ import annotations
import os
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MandiMitra Market Data Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DATA_GOV_URL = "https://api.data.gov.in/resource/"

@app.get("/health")
def health():
    return {"status": "ok", "service": "mandimitra-market-data", "provider": "AGMARKNET via data.gov.in"}

@app.get("/mandi-prices")
def mandi_prices(commodity: str = Query(..., min_length=1), locality: str = Query("Karnataka"), state: Optional[str] = None, limit: int = Query(50, ge=1, le=100)):
    api_key = os.getenv("DATA_GOV_IN_API_KEY", "").strip()
    resource_id = os.getenv("AGMARKNET_RESOURCE_ID", "9ef84268-d588-465a-a308-a864a43d0070").strip()
    if not api_key:
        raise HTTPException(status_code=503, detail="Add DATA_GOV_IN_API_KEY to services/python_api/.env to enable official AGMARKNET records.")
    params = {"api-key": api_key, "format": "json", "limit": limit, "filters[commodity]": commodity}
    if state:
        params["filters[state]"] = state
    try:
        response = requests.get(f"{DATA_GOV_URL}{resource_id}", params=params, timeout=18)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Market data provider request failed: {exc}") from exc
    records = payload.get("records", [])
    # Keep raw source fields; prices are reported as official mandi modal-price records, not tick-by-tick quotes.
    cleaned = []
    for row in records:
        cleaned.append({
            "commodity": row.get("commodity", commodity),
            "market": row.get("market", ""),
            "state": row.get("state", ""),
            "district": row.get("district", ""),
            "arrival_date": row.get("arrival_date", ""),
            "min_price": row.get("min_price", ""),
            "max_price": row.get("max_price", ""),
            "modal_price": row.get("modal_price", ""),
        })
    return {"source": "AGMARKNET / data.gov.in", "data_type": "published_market_arrival_price", "records": cleaned, "count": len(cleaned), "note": "Official mandi records are updated by the source; they are not guaranteed live intraday quotes."}
