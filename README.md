# Grain Intelligence

A React + TypeScript dashboard and FastAPI/PostgreSQL service for grain marketplace workflows, traceable quality records, market-price imports, storage screening and sensor ingestion.

## Run locally (Docker)
1. Copy `.env.example` to `.env`.
2. Set unique random values for `POSTGRES_PASSWORD`, `SECRET_KEY` (at least 32 random bytes) and `IOT_DEVICE_TOKEN`.
3. Run `docker compose up --build` from this directory.
4. Open the frontend at http://localhost:5173 and API docs at http://localhost:8000/docs.
5. Create the first admin from the backend container: `docker compose exec api python -m app.create_admin admin@example.com`.

## Run without Docker
- PostgreSQL must be running and `DATABASE_URL` and `SECRET_KEY` set.
- Backend: `cd backend && pip install -r requirements.txt && alembic upgrade head && uvicorn app.main:app --reload`.
- Frontend: `cd frontend && npm install && npm run dev`.

## Tests
`cd backend && pytest -q`

## Integrated API modules
- `/api/auth`: registration, login and current user.
- `/api/marketplace`: listings and buyer inquiries.
- `/api/orders`: buyer order requests and seller/admin status transitions.
- `/api/certificates`: owner-issued quality records and PDF export. A seller declaration is not a lab certificate.
- `/api/market-data`: historical AGMARKNET/data.gov.in imports; requires resource ID and API key.
- `/api/disease-detection`: image-quality checks only until a validated model is deployed; it never invents a diagnosis.
- `/api/storage/risk-assessment`: transparent threshold-based screening, not shelf-life prediction or food-safety advice.
- `/api/iot/readings`: authenticated device ingestion using `X-Device-Token`; authenticated users can read stored data.
- `/api/assistant`: Ollama tool-assisted chat; requires a reachable Ollama server and pulled model.
- `/api/environment/simulated`: explicitly simulated sensor sample.

## Provenance and production limits
Historical market observations, simulated readings, user-provided sensor readings, rule-based screening and AI/lab records are distinct. No disease model weights or training dataset are included in this repository. No ESP32 firmware, MQTT broker, FAOSTAT integration, real-time price feed, payment gateway, SMS/email notification provider, or independently accredited lab integration is included. Those require external datasets, credentials, hardware, contracts or validation and are not represented as completed.

## Deployment checklist
Use HTTPS and a managed secret store; rotate all secrets; configure production CORS; back up PostgreSQL; add rate limiting and audit logs; use a broker/device identity system for fleets; validate sensor calibration; pin and scan container dependencies; run migrations before rollout; and perform security, load and model validation before production use.
