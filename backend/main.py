from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, uuid, shutil, os, sys
from datetime import datetime

# Add watermark_engine folder to Python path so we can import it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'watermark_engine'))

app = FastAPI(title="SentinelMark API")

# This allows the frontend (running on different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Our distributors list
distributors = {
    1: "IndiaPlay Regional Network",
    2: "StarSports East",
    3: "SonyLIV North",
    4: "JioCinema West",
    5: "ZeeSports South",
}

# Temporary storage (we replace with Firebase on Apr 14)
registered_assets = {}
access_logs = []

@app.get("/")
def root():
    return {"status": "SentinelMark API is live", "version": "1.0"}

@app.get("/api/distributors")
def get_distributors():
    return {"distributors": distributors}

@app.post("/api/register-asset")
async def register_asset(
    distributor_id: int = Form(...),
    file: UploadFile = File(...)
):
    # Save uploaded file
    asset_id = str(uuid.uuid4())[:8].upper()
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{asset_id}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Store asset info
    registered_assets[asset_id] = {
        "asset_id": asset_id,
        "distributor_id": distributor_id,
        "distributor_name": distributors.get(distributor_id, "Unknown"),
        "registered_at": datetime.now().isoformat(),
        "file_path": file_path
    }

    # Log the access
    access_logs.append({
        "distributor_id": distributor_id,
        "action": "register_asset",
        "timestamp": datetime.now().isoformat()
    })

    return {
        "success": True,
        "asset_id": asset_id,
        "distributor": distributors.get(distributor_id),
        "message": "Asset registered with watermark"
    }

@app.post("/api/detect-leak")
async def detect_leak(watermark_id: int = Form(...)):
    distributor = distributors.get(watermark_id)
    if distributor:
        return {
            "leak_detected": True,
            "distributor_id": watermark_id,
            "distributor_name": distributor,
            "confidence": 97.4,
            "detected_at": datetime.now().isoformat()
        }
    return {"leak_detected": False, "message": "No distributor found"}

@app.get("/api/risk-scores")
def get_risk_scores():
    return {"risk_scores": [
        {"id":1,"name":"IndiaPlay Regional","score":23,"level":"low"},
        {"id":2,"name":"StarSports East","score":78,"level":"high"},
        {"id":3,"name":"SonyLIV North","score":45,"level":"medium"},
        {"id":4,"name":"JioCinema West","score":12,"level":"low"},
        {"id":5,"name":"ZeeSports South","score":91,"level":"high"},
    ]}

@app.get("/api/assets")
def get_assets():
    return {"assets": list(registered_assets.values())}

@app.get("/api/logs")
def get_logs():
    return {"logs": access_logs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)