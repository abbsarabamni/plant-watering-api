from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
import os

DATA_FILE = "plants_data.json"

app = FastAPI()

# load or init data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
else:
    # initial data for ۴ گل
    db = {
        "1": {"name": "ندمی (سجافی)", "history": []},
        "2": {"name": "پتوس", "history": []},
        "3": {"name": "پیچک (نیلوفر)", "history": []},
        "4": {"name": "مرجان", "history": []}
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

class WaterRequest(BaseModel):
    plant_id: str

@app.get("/")
def root():
    return {"message": "Plant watering API is running."}

@app.post("/water")
def water(request: WaterRequest):
    pid = request.plant_id
    if pid not in db:
        raise HTTPException(status_code=404, detail="Plant not found")
    now = datetime.utcnow().isoformat()
    db[pid]["history"].append(now)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return {"status": "ok", "plant_id": pid, "timestamp": now}

@app.get("/plant/{pid}")
def get_plant(pid: str):
    if pid not in db:
        raise HTTPException(status_code=404, detail="Plant not found")
    return db[pid]
