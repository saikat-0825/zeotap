#!/bin/bash
echo "🔥 Simulating RDBMS Primary Outage (P0) - Sending 200 concurrent signals..."
for i in {1..200}; do
   curl -s -X POST http://localhost:8000/ingest \
        -H "Content-Type: application/json" \
        -d '{"component_id": "RDBMS_PRIMARY", "error": "CONNECTION_REFUSED", "severity": "P0"}' > /dev/null &
done

echo "⏳ Waiting 2 seconds for cascading effects..."
sleep 2

echo "🔥 Simulating Cache Cluster Timeout (P2) - Sending 50 concurrent signals..."
for i in {1..50}; do
   curl -s -X POST http://localhost:8000/ingest \
        -H "Content-Type: application/json" \
        -d '{"component_id": "CACHE_CLUSTER_01", "error": "TIMEOUT", "severity": "P2"}' > /dev/null &
done

wait
echo "✅ Outage simulation complete. Check your IMS Dashboard at http://localhost:8000/dashboard!"