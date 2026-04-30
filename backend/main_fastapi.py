from fastapi import FastAPI, HTTPException, Request
import time

app = FastAPI()

# ---------------- STORAGE ----------------
signals = []
incidents = {}

# ---------------- CONFIG ----------------
DEBOUNCE_WINDOW = 60   # seconds
RATE_LIMIT = 5         # max requests
WINDOW = 10            # seconds

request_log = {}

# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "IMS Running"}

# ---------------- GET SIGNALS ----------------
@app.get("/signals")
def get_signals():
    return signals

# ---------------- GET INCIDENTS ----------------
@app.get("/incidents")
def get_incidents():
    return incidents

# ---------------- INGEST SIGNAL ----------------
@app.post("/ingest")
def ingest(data: dict, request: Request):
    current_time = time.time()

    # -------- RATE LIMIT --------
    client_ip = request.client.host

    if client_ip not in request_log:
        request_log[client_ip] = []

    # remove old timestamps
    request_log[client_ip] = [
        t for t in request_log[client_ip] if current_time - t < WINDOW
    ]

    if len(request_log[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    request_log[client_ip].append(current_time)

    # -------- SIGNAL PROCESSING --------
    data["timestamp"] = current_time
    signals.append(data)

    comp = data.get("component_id")

    if comp not in incidents:
        incidents[comp] = {
            "component_id": comp,
            "status": "OPEN",
            "signals": [data],
            "start_time": current_time,
            "last_signal_time": current_time,
            "rca": None
        }
        print("🚨 New Incident:", comp)

    else:
        last_time = incidents[comp]["last_signal_time"]

        # -------- DEBOUNCING --------
        if current_time - last_time <= DEBOUNCE_WINDOW:
            incidents[comp]["signals"].append(data)
            incidents[comp]["last_signal_time"] = current_time
            print("➕ Debounced signal:", comp)
        else:
            incidents[comp] = {
                "component_id": comp,
                "status": "OPEN",
                "signals": [data],
                "start_time": current_time,
                "last_signal_time": current_time,
                "rca": None
            }
            print("🚨 New Incident after gap:", comp)

    return {"status": "signal received"}

# ---------------- UPDATE INCIDENT ----------------
@app.post("/update")
def update(data: dict):
    comp = data.get("component_id")
    new_status = data.get("status")
    rca = data.get("rca")

    if comp not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")

    # -------- RCA VALIDATION --------
    if new_status == "CLOSED" and not rca:
        raise HTTPException(status_code=400, detail="RCA required before closing")

    incidents[comp]["status"] = new_status

    if rca:
        incidents[comp]["rca"] = rca
        incidents[comp]["end_time"] = time.time()

        # -------- MTTR --------
        start = incidents[comp]["start_time"]
        end = incidents[comp]["end_time"]
        incidents[comp]["mttr"] = end - start

    return {"status": "updated"}