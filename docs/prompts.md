Prompt 1: Database Setup

"Write a Python database.py file using SQLAlchemy for PostgreSQL (async asyncpg) and Motor for MongoDB. Provide the SQLAlchemy model for an Incident (id, component_id, state, start_time, end_time) and the connection logic."

Prompt 2: The Async Worker

"Write a Python script worker.py using asyncio. It needs to read continuously from a Redis Stream named 'incident_stream' using XREADGROUP. For each message, it should parse the JSON, write the raw payload to a MongoDB collection named 'raw_signals', and if the 'is_new' flag is true, insert a new Incident record into PostgreSQL."

Prompt 3: Base HTMX & Tailwind Setup

"Write a base.html Jinja2 template. Include the CDN links for Tailwind CSS and HTMX. Create a modern, dark-mode styling for an SRE dashboard navigation bar."

Prompt 4: The RCA Form Endpoint

"Write a FastAPI route POST /api/incident/{incident_id}/close that accepts Form data (root_cause_category, fix_applied). It should validate the data to ensure nothing is blank. If it is blank, return an HTML snippet <div class='text-red-500'>Error: RCA is mandatory</div>. If successful, return <div class='text-green-500'>Incident Closed Successfully!</div>."

Prompt 5: The Incident Detail View

"Write a Jinja2 template incident_detail.html styled with Tailwind. It should display the incident metadata at the top, a scrollable div showing raw JSON signals (fetched from MongoDB) in the middle, and the RCA form at the bottom. Use HTMX to submit the RCA form."

Prompt 6: Unit Testing the State Pattern

"Write a pytest file named test_state.py. I have an Incident class using the State Design Pattern. Write a test that initializes an Incident in the ResolvedState. Assert that calling incident.transition_to_closed(rca_data=None) raises a ValueError with the message 'Mandatory RCA is missing'. Write a second test proving that passing valid RCA data (containing 'root_cause_category' and 'fix_applied') successfully transitions the state to ClosedState."

Prompt 7: Comprehensive README

"Write a professional README.md for an Incident Management System. It must include the following sections:

Overview: A brief description.

Architecture: A placeholder for an architecture diagram image.

Handling Backpressure: Explain that the FastAPI ingestion endpoint acts as a producer, immediately pushing JSON payloads to a Redis Stream and returning a 202 Accepted. Explain that a background worker consumes this stream asynchronously to protect PostgreSQL and MongoDB from connection exhaustion during a 10,000 req/sec burst.

Setup Instructions: Step-by-step instructions on how to run docker-compose up --build and execute ./simulate_outage.sh.

Tech Stack: Mention FastAPI, HTMX, Redis, PostgreSQL, and MongoDB."