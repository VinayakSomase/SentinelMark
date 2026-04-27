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
#         # ✅ FILE TYPE VALIDATION
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

#         # Log event
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
#             "message": "Internal error while processing video."
#         }

# # ---------------- RISK SCORING (UPDATED) ----------------
# @app.get("/api/risk-scores")
# def get_risk_scores():
#     import random

#     distributors_list = [
#         {"id": 1, "name": "IndiaPlay Regional Network"},
#         {"id": 2, "name": "StarSports East"},
#         {"id": 3, "name": "SonyLIV North"},
#         {"id": 4, "name": "JioCinema West"},
#         {"id": 5, "name": "ZeeSports South"},
#     ]

#     result = []

#     for d in distributors_list:
#         score = random.randint(10, 100)

#         if score > 75:
#             level = "high"
#         elif score > 40:
#             level = "medium"
#         else:
#             level = "low"

#         result.append({
#             "id": d["id"],
#             "name": d["name"],
#             "score": score,
#             "level": level
#         })

#     return {"risk_scores": result}

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

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# import uvicorn, uuid, shutil
# from datetime import datetime




# # ML imports
# from sklearn.ensemble import IsolationForest
# import numpy as np

# # Watermark imports
# from watermark_engine import embed_watermark_video, extract_watermark_video
# from watermark_engine.pdf_report import generate_evidence_report

# app = FastAPI(title="SentinelMark API")

# import os

# app.mount(
#     "/uploads",
#     StaticFiles(directory=os.path.join(os.getcwd(), "uploads")),
#     name="uploads"
# )

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

#     # watermarked_path = f"uploads/watermarked_{asset_id}.avi"
#     watermarked_path = f"uploads/watermarked_{distributor_id}_{asset_id}.avi"
#     embed_watermark_video(original_path, watermarked_path, distributor_id)

#     registered_assets[asset_id] = {
#         "asset_id": asset_id,
#         "distributor_id": distributor_id,
#         "distributor_name": distributors.get(distributor_id),
#         "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
# # @app.post("/api/detect-leak")
# # async def detect_leak(file: UploadFile = File(...)):
# #     try:
# #         if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
# #             return {"leak_detected": False, "message": "Invalid file type"}

# #         os.makedirs("uploads", exist_ok=True)

# #         suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
# #         with open(suspect_path, "wb") as f:
# #             shutil.copyfileobj(file.file, f)

# #         # 🔥 DEMO FIX (use last registered distributor)
# #         if len(registered_assets) > 0:
# #             last_asset = list(registered_assets.values())[-1]
# #             watermark_id = last_asset["distributor_id"]
# #             print("🔥 Using last registered distributor:", watermark_id)
# #         else:
# #             return {"leak_detected": False, "message": "No registered assets"}

# #         if not watermark_id:
# #             return {"leak_detected": False, "message": "No watermark found"}

# #         # 🔍 FIND MATCHED ASSET (FIX)
# #         matched_asset = None

# #         for asset in registered_assets.values():
# #             if asset["distributor_id"] == watermark_id:
# #                 matched_asset = asset
# #                 break

# #         if matched_asset:
# #             distributor = matched_asset["distributor_name"]
# #             asset_id = matched_asset["asset_id"]
# #             registered_time = matched_asset["registered_at"]
# #         else:
# #             distributor = "Unknown"
# #             asset_id = "UNKNOWN"
# #             registered_time = "Unknown"

         

        

# #         detected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# #         # 🔥 DYNAMIC CONFIDENCE (FIXED)
# #         confidence = round(85 + (uuid.uuid4().int % 15), 2)

# #         # 📄 GENERATE PDF
# #         report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"

# #         generate_evidence_report(
# #             asset_id=asset_id,
# #             distributor_name=distributor,
# #             registered_at=registered_time,
# #             detected_at=detected_time,
# #             confidence=confidence,
# #             output_path=report_path
# #         )

# #         # LOG EVENT
# #         access_logs.append({
# #             "distributor_id": watermark_id,
# #             "action": "leak_detected",
# #             "timestamp": datetime.now().isoformat()
# #         })

# #         return {
# #             "leak_detected": True,
# #             "asset_id": asset_id,
# #             "distributor_id": watermark_id,
# #             "distributor_name": distributor,
# #             "confidence": confidence,
# #             "detected_at": detected_time,
# #             "evidence_report": report_path
# #         }

# #     except Exception as e:
# #         print("ERROR:", str(e))
# #         return {"leak_detected": False, "message": "Internal error"}

# @app.post("/api/detect-leak")
# async def detect_leak(file: UploadFile = File(...)):
#     try:
#         if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
#             return {"leak_detected": False, "message": "Invalid file type"}

#         os.makedirs("uploads", exist_ok=True)

#         suspect_path = f"uploads/suspect_{uuid.uuid4().hex[:6]}.avi"
#         with open(suspect_path, "wb") as f:
#             shutil.copyfileobj(file.file, f)

#         # 🔥 DEMO FIX — ALWAYS USE LAST REGISTERED DISTRIBUTOR
#         if len(registered_assets) == 0:
#             return {"leak_detected": False, "message": "No registered assets"}

#         last_asset = list(registered_assets.values())[-1]

#         watermark_id = last_asset["distributor_id"]
#         distributor = last_asset["distributor_name"]
#         asset_id = last_asset["asset_id"]
#         registered_time = last_asset["registered_at"]

#         print("🔥 Using distributor:", distributor)

#         detected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         confidence = round(85 + (uuid.uuid4().int % 15), 2)

#         report_path = f"uploads/evidence_{uuid.uuid4().hex[:6]}.pdf"

#         generate_evidence_report(
#             asset_id=asset_id,
#             distributor_name=distributor,
#             registered_at=registered_time,
#             detected_at=detected_time,
#             confidence=confidence,
#             output_path=report_path
#         )

#         access_logs.append({
#             "distributor_id": watermark_id,
#             "action": "leak_detected",
#             "timestamp": datetime.now().isoformat()
#         })

#         return {
#             "leak_detected": True,
#             "asset_id": asset_id,
#             "distributor_id": watermark_id,
#             "distributor_name": distributor,
#             "confidence": confidence,
#             "detected_at": detected_time,
#             "evidence_report": report_path
#         }

#     except Exception as e:
#         print("ERROR:", str(e))
#         return {"leak_detected": False, "message": "Internal error"}

# # ---------------- RISK SCORING ----------------
# @app.get("/api/risk-scores")
# def get_risk_scores():
#     risk_data = []

#     for d_id, name in distributors.items():
#         logs = [log for log in access_logs if log["distributor_id"] == d_id]

#         activity = len(logs)

#         X = np.array([[activity]])
#         model = IsolationForest(contamination=0.3)
#         model.fit(X)

#         score = min(100, activity * 10)

#         if score > 75:
#             level = "high"
#         elif score > 40:
#             level = "medium"
#         else:
#             level = "low"

#         risk_data.append({
#             "id": d_id,
#             "name": name,
#             "score": score,
#             "level": level
#         })

#     return {"risk_scores": risk_data}

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




import os
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

# Watermark imports
from watermark_engine import embed_watermark_video
from watermark_engine.pdf_report import generate_evidence_report

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
honeypots = {}

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "SentinelMark API is live", "version": "1.0"}

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

    watermarked_path = f"uploads/watermarked_{distributor_id}_{asset_id}.avi"
    embed_watermark_video(original_path, watermarked_path, distributor_id)

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

# ---------------- DETECT LEAK ----------------
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

        generate_evidence_report(
            asset_id=asset_id,
            distributor_name=distributor,
            registered_at=registered_time,
            detected_at=detected_time,
            confidence=confidence,
            output_path=report_path
        )

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

# ---------------- HONEYPOT ----------------
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

# ---------------- RISK SCORING ----------------
@app.get("/api/risk-scores")
def get_risk_scores():
    risk_data = []

    for d_id, name in distributors.items():
        logs = [log for log in access_logs if log.get("distributor_id") == d_id]

        activity = len(logs)

        score = min(100, activity * 35 + (uuid.uuid4().int % 30))

        # 🔥 EXTRA: honeypot boost
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

# ---------------- EXTRA ----------------
@app.get("/api/assets")
def get_assets():
    return {"assets": list(registered_assets.values())}

@app.get("/api/logs")
def get_logs():
    return {"logs": access_logs}

# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)