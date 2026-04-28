# SentinelMark  
# AI-Powered Anti-Piracy & Leak Detection System  

*Live Demo:* https://sentinel-mark.vercel.app/  


#  Overview

SentinelMark protects sports media by embedding invisible watermarks, predicting leaks before they happen, and
proactively trapping piracy networks.
  
It combines **invisible watermarking**, **honeypot traps**, and **behavioral risk analytics** to identify suspicious distributors and prevent large-scale piracy.


# Problem Statement

"Sports organizations distribute official media to authorized broadcasters. This content gets leaked and pirated before official broadcast windows, causing massive revenue loss. No accessible tool exists to identify the source of a leak forensically, predict which distributor will leak, or map the piracy networks distributing stolen content."


# Our Solution

SentinelMark solves this problem by:

"SentinelMark is a three-layer intelligent protection system. 
Layer 1 embeds unique invisible watermarks per distributor and identifies leak sources forensically. 
Layer 2 monitors access behavior using anomaly detection to predict leaks before they happen. 
Layer 3 generates AI-modified honeypot content variants to proactively map piracy distribution networks."


# Key Features

# Asset Registration
- Upload digital content  
- Assign unique distributor identity  
- Embed invisible watermark  

# Leak Detection
- Analyze suspicious or leaked content  
- Extract watermark signature  
- Identify source distributor  

# Honeypot Tracking
- Create hidden traps for attackers  
- Detect unauthorized access  
- Log suspicious activity  

# Risk Monitoring Dashboard
- Real-time risk scoring  
- Activity-based analytics  
- Automatic high-risk flagging  



# System Architecture

Frontend (React - Vercel)
↓
Backend API (FastAPI - Google Cloud Run)
↓
Watermarking + Detection + Risk Engine


# Tech Stack

| Layer        | Technology                       |
|------------- |----------------------------------|               
| Frontend     | React.js (Vercel)                |
| Backend      | FastAPI (Google Cloud Run)       |
| AI Model     | Isolation Forest (Risk Scoring)  |
| Deployment   | Vercel + Google Cloud Run        |


# Limitations (MVP Scope)

- Uses **temporary (ephemeral) storage** in Cloud Run  
- Watermark processing optimized for demo performance  
- Persistent storage (e.g., Google Cloud Storage) can be added in production  


# Future Enhancements

- Integration with **Google Cloud Storage (GCS)**  
- DCT-domain watermarking for Phase 2   
- Real-time alert system  
- Multi-distributor tracking dashboard  


# 🎬 Demo Flow

1. Register Asset → Watermark embedded  
2. Detect Leak → Source identified  
3. Honeypot → Simulated attack detection  
4. Risk Monitor → View real-time analytics  


# 👨‍💻 Team Members 

Bhupesh Patil
Vinayak Somase 
Chanchal Bachhav


#  Conclusion

SentinelMark is an intelligent digital asset protection system that predicts potential leaks before they happen, forensically identifies the source of any leak, and proactively traps piracy networks using AI-generated honeypot content.


*Built for Google Solution Challenge 2026*

 Thank You.