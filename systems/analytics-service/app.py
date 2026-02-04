from fastapi import FastAPI
from typing import Dict

app = FastAPI(title="Analytics Service")

@app.post("/analytics/data")
def receive_analytics(data: Dict):
    print("📊 Analytics received:", data)
    return {"status": "processed"}

@app.get("/health")
def health():
    return {"status": "ok",
            "service": "analytics-service"
            }
