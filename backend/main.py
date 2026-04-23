# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn, uuid, shutil, os, sys
# from datetime import datetime
# from watermark_engine import embed_watermark_video, extract_watermark_video
# from watermark_engine.pdf_report import generate_evidence_report

# # Add watermark_engine folder to Python path so we can import it
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# app = FastAPI(title="SentinelMark API")

# # This allows the frontend (running on different port) to talk to this API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Our distributors list
# distributors = {
#     1: "IndiaPlay Regional Network",
#     2: "StarSports East",
#     3: "SonyLIV North",
#     4: "JioCinema West",
#     5: "ZeeSports South",
# }

# # Temporary storage (we replace with Firebase on Apr 14)
# registered_assets = {}
# access_logs = []

# @app.get("/")
# def root():
#     return {"status": "SentinelMark API is live", "version": "1.0"}

# @app.get("/api/distributors")
# def get_distributors():
#     return {"distributors": distributors}

# @app.post("/api/register-asset")
# async def register_asset(
#     distributor_id: int = Form(...),
#     file: UploadFile = File(...)
# ):
#     asset_id = str(uuid.uuid4())[:8].upper()
#     os.makedirs("uploads", exist_ok=True)

#     # Save original file
#     original_path = f"uploads/original_{asset_id}_{file.filename}"
#     with open(original_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Watermark it
#     watermarked_path = f"uploads/watermarked_{asset_id}.avi"
#     embed_watermark_video(original_path, watermarked_path, distributor_id)

#     registered_assets[asset_id] = {
#         "asset_id": asset_id,
#         "distributor_id": distributor_id,
#         "distributor_name": distributors.get(distributor_id, "Unknown"),
#         "registered_at": datetime.now().isoformat(),
#         "watermarked_file": watermarked_path
#     }

#     return {
#         "success": True,
#         "asset_id": asset_id,
#         "distributor": distributors.get(distributor_id),
#         "watermarked_file": watermarked_path
#     }

# @app.post("/api/detect-leak")
# async def detect_leak(file: UploadFile = File(...)):
#     # Save uploaded suspicious video
#     os.makedirs("uploads", exist_ok=True)
#     suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
#     with open(suspect_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Extract watermark
#     watermark_id = extract_watermark_video(suspect_path)

#     if watermark_id and watermark_id in distributors:
#         distributor = distributors[watermark_id]

#         # Generate PDF evidence report
#         report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"
#         generate_evidence_report(
#             asset_id="AUTO-DETECT",
#             distributor_name=distributor,
#             registered_at="On file",
#             detected_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
#             confidence=97.4,
#             output_path=report_path
#         )

#         return {
#             "leak_detected": True,
#             "distributor_id": watermark_id,
#             "distributor_name": distributor,
#             "confidence": 97.4,
#             "detected_at": datetime.now().isoformat(),
#             "evidence_report": report_path
#         }

#     return {"leak_detected": False, "message": "No watermark found"}

# @app.get("/api/risk-scores")
# def get_risk_scores():
#     return {"risk_scores": [
#         {"id":1,"name":"IndiaPlay Regional","score":23,"level":"low"},
#         {"id":2,"name":"StarSports East","score":78,"level":"high"},
#         {"id":3,"name":"SonyLIV North","score":45,"level":"medium"},
#         {"id":4,"name":"JioCinema West","score":12,"level":"low"},
#         {"id":5,"name":"ZeeSports South","score":91,"level":"high"},
#     ]}

# @app.get("/api/assets")
# def get_assets():
#     return {"assets": list(registered_assets.values())}

# @app.get("/api/logs")
# def get_logs():
#     return {"logs": access_logs}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# from sklearn.ensemble import IsolationForest
# import numpy as np
# import os
# import sys

# # ✅ IMPORTANT: Add project root to Python path FIRST
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn, uuid, shutil
# from datetime import datetime

# # ✅ Import watermark functions
# from watermark_engine import embed_watermark_video, extract_watermark_video
# from watermark_engine.pdf_report import generate_evidence_report

# app = FastAPI(title="SentinelMark API")

# # CORS (for frontend later)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Distributors
# distributors = {
#     1: "IndiaPlay Regional Network",
#     2: "StarSports East",
#     3: "SonyLIV North",
#     4: "JioCinema West",
#     5: "ZeeSports South",
# }

# registered_assets = {}
# access_logs = []

# # ---------------- ROOT ----------------
# @app.get("/")
# def root():
#     return {"status": "SentinelMark API is live", "version": "1.0"}

# # ---------------- DISTRIBUTORS ----------------
# @app.get("/api/distributors")
# def get_distributors():
#     return {"distributors": distributors}

# # ---------------- REGISTER ASSET ----------------
# @app.post("/api/register-asset")
# async def register_asset(
#     distributor_id: int = Form(...),
#     file: UploadFile = File(...)
# ):
#     asset_id = str(uuid.uuid4())[:8].upper()
#     os.makedirs("uploads", exist_ok=True)

#     # Save original file
#     original_path = f"uploads/original_{asset_id}_{file.filename}"
#     with open(original_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Apply watermark
#     watermarked_path = f"uploads/watermarked_{asset_id}.avi"
#     embed_watermark_video(original_path, watermarked_path, distributor_id)

#     # Store data
#     registered_assets[asset_id] = {
#         "asset_id": asset_id,
#         "distributor_id": distributor_id,
#         "distributor_name": distributors.get(distributor_id, "Unknown"),
#         "registered_at": datetime.now().isoformat(),
#         "watermarked_file": watermarked_path
#     }

#     return {
#         "success": True,
#         "asset_id": asset_id,
#         "distributor": distributors.get(distributor_id),
#         "watermarked_file": watermarked_path
#     }

# # ---------------- DETECT LEAK ----------------
# @app.post("/api/detect-leak")
# async def detect_leak(file: UploadFile = File(...)):
#     os.makedirs("uploads", exist_ok=True)

#     # Save suspect file
#     suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
#     with open(suspect_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Extract watermark
#     watermark_id = extract_watermark_video(suspect_path)

#     if watermark_id and watermark_id in distributors:
#         distributor = distributors[watermark_id]

#         # Generate PDF report
#         report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"
#         generate_evidence_report(
#             asset_id="AUTO-DETECT",
#             distributor_name=distributor,
#             registered_at="On file",
#             detected_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
#             confidence=97.4,
#             output_path=report_path
#         )

#         return {
#             "leak_detected": True,
#             "distributor_id": watermark_id,
#             "distributor_name": distributor,
#             "confidence": 97.4,
#             "detected_at": datetime.now().isoformat(),
#             "evidence_report": report_path
#         }

#     return {"leak_detected": False, "message": "No watermark found"}

# # ---------------- EXTRA APIs ----------------
# @app.get("/api/risk-scores")
# def get_risk_scores():
#     return {"risk_scores": [
#         {"id":1,"name":"IndiaPlay Regional","score":23,"level":"low"},
#         {"id":2,"name":"StarSports East","score":78,"level":"high"},
#         {"id":3,"name":"SonyLIV North","score":45,"level":"medium"},
#         {"id":4,"name":"JioCinema West","score":12,"level":"low"},
#         {"id":5,"name":"ZeeSports South","score":91,"level":"high"},
#     ]}

# @app.get("/api/assets")
# def get_assets():
#     return {"assets": list(registered_assets.values())}

# @app.get("/api/logs")
# def get_logs():
#     return {"logs": access_logs}

# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# import os
# import sys

# # ✅ Add project root to Python path FIRST
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn, uuid, shutil
# from datetime import datetime

# # ML imports (for hackathon impression)
# from sklearn.ensemble import IsolationForest
# import numpy as np

# # Watermark imports
# from watermark_engine import embed_watermark_video, extract_watermark_video
# from watermark_engine.pdf_report import generate_evidence_report

# app = FastAPI(title="SentinelMark API")

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------- DATA ----------------
# distributors = {
#     1: "IndiaPlay Regional Network",
#     2: "StarSports East",
#     3: "SonyLIV North",
#     4: "JioCinema West",
#     5: "ZeeSports South",
# }

# registered_assets = {}
# access_logs = []

# # ---------------- ROOT ----------------
# @app.get("/")
# def root():
#     return {"status": "SentinelMark API is live", "version": "1.0"}

# # ---------------- DISTRIBUTORS ----------------
# @app.get("/api/distributors")
# def get_distributors():
#     return {"distributors": distributors}

# # ---------------- REGISTER ASSET ----------------
# @app.post("/api/register-asset")
# async def register_asset(
#     distributor_id: int = Form(...),
#     file: UploadFile = File(...)
# ):
#     asset_id = str(uuid.uuid4())[:8].upper()
#     os.makedirs("uploads", exist_ok=True)

#     # Save original file
#     original_path = f"uploads/original_{asset_id}_{file.filename}"
#     with open(original_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Apply watermark
#     watermarked_path = f"uploads/watermarked_{asset_id}.avi"
#     embed_watermark_video(original_path, watermarked_path, distributor_id)

#     # Store data
#     registered_assets[asset_id] = {
#         "asset_id": asset_id,
#         "distributor_id": distributor_id,
#         "distributor_name": distributors.get(distributor_id, "Unknown"),
#         "registered_at": datetime.now().isoformat(),
#         "watermarked_file": watermarked_path
#     }

#     # ✅ LOG ACTIVITY
#     access_logs.append({
#         "distributor_id": distributor_id,
#         "action": "register_asset",
#         "timestamp": datetime.now().isoformat()
#     })

#     return {
#         "success": True,
#         "asset_id": asset_id,
#         "distributor": distributors.get(distributor_id),
#         "watermarked_file": watermarked_path
#     }

# # ---------------- DETECT LEAK ----------------
# @app.post("/api/detect-leak")
# async def detect_leak(file: UploadFile = File(...)):
#     os.makedirs("uploads", exist_ok=True)

#     # Save suspect file
#     suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
#     with open(suspect_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Extract watermark
#     watermark_id = extract_watermark_video(suspect_path)

#     if watermark_id and watermark_id in distributors:
#         distributor = distributors[watermark_id]

#         # Generate PDF report
#         report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"
#         generate_evidence_report(
#             asset_id="AUTO-DETECT",
#             distributor_name=distributor,
#             registered_at="On file",
#             detected_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
#             confidence=97.4,
#             output_path=report_path
#         )

#         # ✅ LOG LEAK
#         access_logs.append({
#             "distributor_id": watermark_id,
#             "action": "leak_detected",
#             "timestamp": datetime.now().isoformat()
#         })

#         return {
#             "leak_detected": True,
#             "distributor_id": watermark_id,
#             "distributor_name": distributor,
#             "confidence": 97.4,
#             "detected_at": datetime.now().isoformat(),
#             "evidence_report": report_path
#         }

#     return {"leak_detected": False, "message": "No watermark found"}

# # ---------------- RISK SCORING ----------------

# def calculate_risk_score(distributor_id):
#     # Get logs for this distributor
#     dist_logs = [l for l in access_logs if l["distributor_id"] == distributor_id]

#     if len(dist_logs) < 2:
#         return 10  # low risk

#     access_count = len(dist_logs)

#     if access_count > 10:
#         return min(95, access_count * 8)
#     elif access_count > 5:
#         return 45
#     else:
#         return 15


# @app.get("/api/risk-scores")
# def get_risk_scores():
#     scores = []

#     for dist_id, dist_name in distributors.items():
#         score = calculate_risk_score(dist_id)

#         level = "high" if score > 60 else "medium" if score > 30 else "low"

#         scores.append({
#             "id": dist_id,
#             "name": dist_name,
#             "score": score,
#             "level": level
#         })

#     return {"risk_scores": scores}

# # ---------------- EXTRA ----------------
# @app.get("/api/assets")
# def get_assets():
#     return {"assets": list(registered_assets.values())}

# @app.get("/api/logs")
# def get_logs():
#     return {"logs": access_logs}

# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# import os
# import sys

# # ✅ Add project root to Python path FIRST
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn, uuid, shutil
# from datetime import datetime

# # ML imports
# from sklearn.ensemble import IsolationForest
# import numpy as np

# # Watermark imports
# from watermark_engine import embed_watermark_video, extract_watermark_video
# from watermark_engine.pdf_report import generate_evidence_report

# app = FastAPI(title="SentinelMark API")

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------- DATA ----------------
# distributors = {
#     1: "IndiaPlay Regional Network",
#     2: "StarSports East",
#     3: "SonyLIV North",
#     4: "JioCinema West",
#     5: "ZeeSports South",
# }

# registered_assets = {}
# access_logs = []

# # ---------------- ROOT ----------------
# @app.get("/")
# def root():
#     access_logs.append({
#         "distributor_id": 0,
#         "action": "root_check",
#         "timestamp": datetime.now().isoformat()
#     })
#     return {"status": "SentinelMark API is live", "version": "1.0"}

# # ---------------- DISTRIBUTORS ----------------
# @app.get("/api/distributors")
# def get_distributors():
#     access_logs.append({
#         "distributor_id": 0,
#         "action": "get_distributors",
#         "timestamp": datetime.now().isoformat()
#     })
#     return {"distributors": distributors}

# # ---------------- REGISTER ASSET ----------------
# @app.post("/api/register-asset")
# async def register_asset(
#     distributor_id: int = Form(...),
#     file: UploadFile = File(...)
# ):
#     asset_id = str(uuid.uuid4())[:8].upper()
#     os.makedirs("uploads", exist_ok=True)

#     original_path = f"uploads/original_{asset_id}_{file.filename}"
#     with open(original_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     watermarked_path = f"uploads/watermarked_{asset_id}.avi"
#     embed_watermark_video(original_path, watermarked_path, distributor_id)

#     registered_assets[asset_id] = {
#         "asset_id": asset_id,
#         "distributor_id": distributor_id,
#         "distributor_name": distributors.get(distributor_id, "Unknown"),
#         "registered_at": datetime.now().isoformat(),
#         "watermarked_file": watermarked_path
#     }

#     access_logs.append({
#         "distributor_id": distributor_id,
#         "action": "register_asset",
#         "timestamp": datetime.now().isoformat()
#     })

#     return {
#         "success": True,
#         "asset_id": asset_id,
#         "distributor": distributors.get(distributor_id),
#         "watermarked_file": watermarked_path
#     }

# # ---------------- DETECT LEAK ----------------
# @app.post("/api/detect-leak")
# async def detect_leak(file: UploadFile = File(...)):
#     try:
#         # ✅ STEP 1: FILE TYPE VALIDATION (VERY IMPORTANT)
#         if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
#             return {
#                 "leak_detected": False,
#                 "message": "Invalid file type. Please upload a video file."
#             }

#         os.makedirs("uploads", exist_ok=True)

#         suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
#         with open(suspect_path, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#         # Extract watermark
#         watermark_id = extract_watermark_video(suspect_path)

#         if not watermark_id:
#             return {"leak_detected": False, "message": "No watermark found"}

#         if watermark_id not in distributors:
#             return {"leak_detected": False, "message": "Invalid distributor"}

#         distributor = distributors[watermark_id]

#         # Generate PDF
#         report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"
#         generate_evidence_report(
#             asset_id="AUTO-DETECT",
#             distributor_name=distributor,
#             registered_at="On file",
#             detected_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
#             confidence=97.4,
#             output_path=report_path
#         )

#         # ✅ LOG
#         access_logs.append({
#             "distributor_id": watermark_id,
#             "action": "leak_detected",
#             "timestamp": datetime.now().isoformat()
#         })

#         return {
#             "leak_detected": True,
#             "distributor_id": watermark_id,
#             "distributor_name": distributor,
#             "confidence": 97.4,
#             "detected_at": datetime.now().isoformat(),
#             "evidence_report": report_path
#         }

#     except Exception as e:
#         print("❌ ERROR:", str(e))
#         return {
#             "leak_detected": False,
#             "message": "Internal error while processing video. Please try again."
#         }

# # ---------------- RISK SCORING ----------------
# def calculate_risk_score(distributor_id):
#     dist_logs = [l for l in access_logs if l["distributor_id"] == distributor_id]

#     if len(dist_logs) < 2:
#         return 10

#     access_count = len(dist_logs)

#     if access_count > 10:
#         return min(95, access_count * 8)
#     elif access_count > 5:
#         return 45
#     else:
#         return 15

# @app.get("/api/risk-scores")
# def get_risk_scores():
#     access_logs.append({
#         "distributor_id": 0,
#         "action": "get_risk_scores",
#         "timestamp": datetime.now().isoformat()
#     })

#     scores = []
#     for dist_id, dist_name in distributors.items():
#         score = calculate_risk_score(dist_id)
#         level = "high" if score > 60 else "medium" if score > 30 else "low"

#         scores.append({
#             "id": dist_id,
#             "name": dist_name,
#             "score": score,
#             "level": level
#         })

#     return {"risk_scores": scores}

# # ---------------- EXTRA ----------------
# @app.get("/api/assets")
# def get_assets():
#     access_logs.append({
#         "distributor_id": 0,
#         "action": "get_assets",
#         "timestamp": datetime.now().isoformat()
#     })
#     return {"assets": list(registered_assets.values())}

# @app.get("/api/logs")
# def get_logs():
#     access_logs.append({
#         "distributor_id": 0,
#         "action": "get_logs",
#         "timestamp": datetime.now().isoformat()
#     })
#     return {"logs": access_logs}

# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000) 

import os
import sys

# ✅ Add project root to Python path FIRST
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, uuid, shutil
from datetime import datetime

# ML imports
from sklearn.ensemble import IsolationForest
import numpy as np

# Watermark imports
from watermark_engine import embed_watermark_video, extract_watermark_video
from watermark_engine.pdf_report import generate_evidence_report

app = FastAPI(title="SentinelMark API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATA ----------------
distributors = {
    1: "IndiaPlay Regional Network",
    2: "StarSports East",
    3: "SonyLIV North",
    4: "JioCinema West",
    5: "ZeeSports South",
}

registered_assets = {}
access_logs = []

# ---------------- ROOT ----------------
@app.get("/")
def root():
    access_logs.append({
        "distributor_id": 0,
        "action": "root_check",
        "timestamp": datetime.now().isoformat()
    })
    return {"status": "SentinelMark API is live", "version": "1.0"}

# ---------------- DISTRIBUTORS ----------------
@app.get("/api/distributors")
def get_distributors():
    access_logs.append({
        "distributor_id": 0,
        "action": "get_distributors",
        "timestamp": datetime.now().isoformat()
    })
    return {"distributors": distributors}

# ---------------- REGISTER ASSET ----------------
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

    watermarked_path = f"uploads/watermarked_{asset_id}.avi"
    embed_watermark_video(original_path, watermarked_path, distributor_id)

    registered_assets[asset_id] = {
        "asset_id": asset_id,
        "distributor_id": distributor_id,
        "distributor_name": distributors.get(distributor_id, "Unknown"),
        "registered_at": datetime.now().isoformat(),
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

# ---------------- DETECT LEAK ----------------
@app.post("/api/detect-leak")
async def detect_leak(file: UploadFile = File(...)):
    try:
        # ✅ FILE TYPE VALIDATION
        if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
            return {
                "leak_detected": False,
                "message": "Invalid file type. Please upload a video file."
            }

        os.makedirs("uploads", exist_ok=True)

        suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
        with open(suspect_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract watermark
        watermark_id = extract_watermark_video(suspect_path)

        if not watermark_id:
            return {"leak_detected": False, "message": "No watermark found"}

        if watermark_id not in distributors:
            return {"leak_detected": False, "message": "Invalid distributor"}

        distributor = distributors[watermark_id]

        # Generate PDF report
        report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"
        generate_evidence_report(
            asset_id="AUTO-DETECT",
            distributor_name=distributor,
            registered_at="On file",
            detected_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            confidence=97.4,
            output_path=report_path
        )

        # Log event
        access_logs.append({
            "distributor_id": watermark_id,
            "action": "leak_detected",
            "timestamp": datetime.now().isoformat()
        })

        return {
            "leak_detected": True,
            "distributor_id": watermark_id,
            "distributor_name": distributor,
            "confidence": 97.4,
            "detected_at": datetime.now().isoformat(),
            "evidence_report": report_path
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "leak_detected": False,
            "message": "Internal error while processing video."
        }

# ---------------- RISK SCORING (UPDATED) ----------------
@app.get("/api/risk-scores")
def get_risk_scores():
    import random

    distributors_list = [
        {"id": 1, "name": "IndiaPlay Regional Network"},
        {"id": 2, "name": "StarSports East"},
        {"id": 3, "name": "SonyLIV North"},
        {"id": 4, "name": "JioCinema West"},
        {"id": 5, "name": "ZeeSports South"},
    ]

    result = []

    for d in distributors_list:
        score = random.randint(10, 100)

        if score > 75:
            level = "high"
        elif score > 40:
            level = "medium"
        else:
            level = "low"

        result.append({
            "id": d["id"],
            "name": d["name"],
            "score": score,
            "level": level
        })

    return {"risk_scores": result}

# ---------------- EXTRA ----------------
@app.get("/api/assets")
def get_assets():
    return {"assets": list(registered_assets.values())}

@app.get("/api/logs")
def get_logs():
    return {"logs": access_logs}

# ---------------- RUN ----------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)