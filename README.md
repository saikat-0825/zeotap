# Mission-Critical Incident Management System (IMS)

## Overview
This is a resilient Incident Management System designed to monitor a distributed stack. It handles high-volume error signals using asynchronous processing, manages failure mediation workflows via robust design patterns, and provides a real-time HTMX dashboard.

## Handling Backpressure
To prevent database connection exhaustion during bursts of up to 10,000 signals/sec, this system utilizes an **In-Memory Buffer Strategy**:
1. The FastAPI `/ingest` endpoint acts purely as a producer. It validates the signal, performs a quick debounce check against Redis, pushes the raw payload onto a **Redis Stream**, and immediately returns a `202 Accepted`.
2. A background `worker.py` asynchronously consumes this Redis stream, handling the heavy lifting of writing unstructured data to MongoDB and structured transactional data to PostgreSQL with exponential backoff retries.

## Setup Instructions
1. **Start the infrastructure:**
   ```bash
   docker-compose up --build -d