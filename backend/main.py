from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import redis.asyncio as redis
import json
import os
from database import init_db, AsyncSessionLocal, IncidentModel
from sqlalchemy import select

app = FastAPI(title="IMS API")
templates = Jinja2Templates(directory="templates")
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/ingest")
async def ingest_signal(payload: dict):
    component_id = payload.get("component_id", "UNKNOWN")
    debounce_key = f"active:{component_id}"
    is_active = await redis_client.exists(debounce_key)
    
    await redis_client.xadd(
        "incident_stream", 
        {"payload": json.dumps(payload), "is_new": str(not is_active)}
    )
    
    if not is_active:
        await redis_client.setex(debounce_key, 10, "active")
        
    return {"status": "Accepted"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/partials/active-incidents", response_class=HTMLResponse)
async def get_active_incidents(request: Request):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(IncidentModel).where(IncidentModel.state != "CLOSED"))
        incidents = result.scalars().all()
    return templates.TemplateResponse("incident_row.html", {"request": request, "incidents": incidents})

@app.post("/api/incident/{incident_id}/close", response_class=HTMLResponse)
async def close_incident(incident_id: str, root_cause_category: str = Form(...), fix_applied: str = Form(...)):
    from patterns.state import WorkflowState
    rca_data = {"root_cause_category": root_cause_category, "fix_applied": fix_applied}
    try:
        new_state = WorkflowState().close_incident(rca_data)
        async with AsyncSessionLocal() as db:
            incident = await db.get(IncidentModel, incident_id)
            if incident:
                incident.state = new_state
                incident.rca_data = rca_data
                await db.commit()
        return f"<div class='p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50'>Incident {incident_id} successfully closed!</div>"
    except ValueError as e:
        return f"<div class='p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50'>Error: {str(e)}</div>"