import asyncio
import json
import uuid
import os
import redis.asyncio as redis
from tenacity import retry, wait_exponential
from database import AsyncSessionLocal, raw_signals_collection, IncidentModel
from patterns.strategy import get_alert_strategy

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
async def save_to_dbs(payload: dict, is_new: bool):
    await raw_signals_collection.insert_one(payload)
    if is_new:
        incident_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
        async with AsyncSessionLocal() as db:
            new_incident = IncidentModel(
                id=incident_id,
                component_id=payload.get("component_id"),
                severity=payload.get("severity"),
                state="OPEN"
            )
            db.add(new_incident)
            await db.commit()
        strategy = get_alert_strategy(payload.get("severity"))
        strategy.trigger_alert(payload.get("component_id"), payload.get("error"))

async def process_stream():
    print("👷 Worker started. Listening to Redis stream 'incident_stream'...")
    last_id = '0'
    while True:
        try:
            messages = await redis_client.xread({"incident_stream": last_id}, count=100, block=2000)
            for stream, msgs in messages:
                for msg_id, msg_data in msgs:
                    payload = json.loads(msg_data[b'payload'].decode('utf-8'))
                    is_new = msg_data[b'is_new'].decode('utf-8') == 'True'
                    await save_to_dbs(payload, is_new)
                    last_id = msg_id
        except Exception as e:
            print(f"Worker Error: {e}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(process_stream())