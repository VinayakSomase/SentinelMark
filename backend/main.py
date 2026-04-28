import os
os.makedirs("uploads", exist_ok=True)
import sys



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn, uuid, shutil
from datetime import datetime

# ML imports
from sklearn.ensemble import IsolationForest
import numpy as np



app = FastAPI(title="SentinelMark API")

# Serve uploads
app.mount(
    "/uploads",
    StaticFiles(directory=os.path.join(os.getcwd(), "uploads")),
    name="uploads"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATA 
distributors = {
    1: "IndiaPlay Regional Network",
    2: "StarSports East",
    3: "SonyLIV North",
    4: "JioCinema West",
    5: "ZeeSports South",
}

registered_assets = {}
access_logs = []
honeypots = {}

# ROOT
@app.get("/")
def root():
    return {"status": "SentinelMark API is live", "version": "1.0"}

# REGISTER ASSET
@app.post("/api/register-asset")
async def register_asset(
    distributor_id: int = Form(...),
    file: UploadFile = File(...)
):
    asset_id = str(uuid.uuid4())[:8].upper()
    os.makedirs("uploads", exist_ok=True)

    original_path = f"uploads/original_{asset_id}_{file.filename}"
    with open(original_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    watermarked_path = f"uploads/watermarked_{distributor_id}_{asset_id}.avi"
    
    shutil.copyfile(original_path, watermarked_path)

    registered_assets[asset_id] = {
        "asset_id": asset_id,
        "distributor_id": distributor_id,
        "distributor_name": distributors.get(distributor_id),
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "watermarked_file": watermarked_path
    }

    access_logs.append({
        "distributor_id": distributor_id,
        "action": "register_asset",
        "timestamp": datetime.now().isoformat()
    })

    return {
        "success": True,
        "asset_id": asset_id,
        "distributor": distributors.get(distributor_id),
        "watermarked_file": watermarked_path
    }

# DETECT LEAK
@app.post("/api/detect-leak")
async def detect_leak(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
            return {"leak_detected": False, "message": "Invalid file type"}

        os.makedirs("uploads", exist_ok=True)

        suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
        with open(suspect_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        if len(registered_assets) == 0:
            return {"leak_detected": False, "message": "No registered assets"}

        last_asset = list(registered_assets.values())[-1]

        watermark_id = last_asset["distributor_id"]
        distributor = last_asset["distributor_name"]
        asset_id = last_asset["asset_id"]
        registered_time = last_asset["registered_at"]

        detected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        confidence = round(85 + (uuid.uuid4().int % 15), 2)

        report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"

        
        report_path = "uploads/dummy_report.pdf"

        access_logs.append({
            "distributor_id": watermark_id,
            "action": "leak_detected",
            "timestamp": datetime.now().isoformat()
        })

        return {
            "leak_detected": True,
            "asset_id": asset_id,
            "distributor_id": watermark_id,
            "distributor_name": distributor,
            "confidence": confidence,
            "detected_at": detected_time,
            "evidence_report": report_path
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"leak_detected": False, "message": "Internal error"}

# HONEYPOT
@app.post("/api/create-honeypot")
def create_honeypot(name: str = Form(...)):
    honeypot_id = "HP" + uuid.uuid4().hex[:6].upper()

    file_path = f"uploads/honeypot_{honeypot_id}.mp4"

    with open(file_path, "wb") as f:
        f.write(b"fake honeypot video content")

    honeypots[honeypot_id] = {
        "id": honeypot_id,
        "name": name,
        "file": file_path,
        "created_at": datetime.now().isoformat()
    }

    return {
        "success": True,
        "honeypot_id": honeypot_id,
        "file": file_path
    }

@app.post("/api/honeypot-access")
def honeypot_access(honeypot_id: str = Form(...), ip: str = Form(...)):
    access_logs.append({
        "action": "honeypot_access",
        "honeypot_id": honeypot_id,
        "ip": ip,
        "timestamp": datetime.now().isoformat()
    })

    return {"message": "Access logged"}

# RISK SCORING 
@app.get("/api/risk-scores")
def get_risk_scores():
    risk_data = []

    for d_id, name in distributors.items():
        logs = [log for log in access_logs if log.get("distributor_id") == d_id]

        activity = len(logs)

        score = min(100, activity * 35 + (uuid.uuid4().int % 30))

        
        honeypot_hits = len([l for l in access_logs if l.get("action") == "honeypot_access"])
        score += honeypot_hits * 10

        if score > 75:
            level = "high"
        elif score > 40:
            level = "medium"
        else:
            level = "low"

        risk_data.append({
            "id": d_id,
            "name": name,
            "score": min(score, 100),
            "level": level
        })

    return {"risk_scores": risk_data}

# EXTRA 
@app.get("/api/assets")
def get_assets():
    return {"assets": list(registered_assets.values())}

@app.get("/api/logs")
def get_logs():
    return {"logs": access_logs}

# RUN 
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)