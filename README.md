# 🚀 Incident Management System (IMS)

A lightweight **Incident Management System backend** built using FastAPI that simulates real-world SRE/DevOps workflows such as signal ingestion, incident grouping, debouncing, rate limiting, RCA enforcement, and MTTR calculation.

---

## 📌 Features

### ✅ Core Functionality
- Signal ingestion via REST API
- Automatic incident creation per component
- Incident lifecycle management (OPEN → CLOSED)
- RCA (Root Cause Analysis) enforcement before closing incidents
- MTTR (Mean Time To Resolve) calculation

### ⚙️ Reliability Engineering Features
- 🔁 **Debouncing Logic**
  - Groups multiple alerts into a single incident within a time window
- 🚦 **Rate Limiting**
  - Prevents API abuse (max 5 requests per 10 seconds)
- 📊 Signal tracking and history per incident

---

## 🧠 System Design Concepts Used

- Event-driven signal processing
- Time-window based deduplication (debouncing)
- In-memory incident store (simulating lightweight monitoring system)
- Stateless REST API design
- Basic SRE principles (alert fatigue reduction, RCA enforcement)

---

## 🛠 Tech Stack

- Python 3.14
- FastAPI
- Uvicorn

---

## 📁 Project Structure
ims_project/
│
├── backend/
│ ├── main_fastapi.py # Core backend API
│
├── .gitignore
└── README.md

---

## 🚀 How to Run Locally

### 1️⃣ Install dependencies
```bash
pip install fastapi uvicorn
python -m uvicorn main_fastapi:app --reload --port 9000
🧪 Key Behaviors
🔁 Debouncing
Multiple signals within 60 seconds are grouped into one incident
Prevents alert flooding
🚦 Rate Limiting
Max 5 requests per 10 seconds per client
Prevents API abuse
MTTR Calculation
Automatically computed when incident is closed:
MTTR = end_time - start_time
