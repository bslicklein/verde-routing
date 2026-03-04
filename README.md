# Verde Truck Routing Optimization POC

AI-powered route optimization for landscaping operations using Google OR-Tools VRP solver. Demonstrates 40%+ reduction in drive time and distance vs naive routing for Phoenix and San Diego regions.

## Quick Start

### Backend
```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev -- -p 3001
```

Open http://localhost:3001, click **Optimize Routes**.

## Tech Stack

- **Frontend:** Next.js 14, Tailwind CSS, Leaflet/OpenStreetMap, Zustand
- **Backend:** FastAPI, Google OR-Tools (CVRPTW solver), OSRM (road distances)
- **No API keys required** - uses free OpenStreetMap tiles and public OSRM server

## Features

- VRP optimization with time windows, equipment matching, and crew capacity constraints
- Color-coded route visualization on interactive map
- Before/after comparison vs naive (round-robin) routing
- Region toggle (Phoenix / San Diego)
- Re-optimization for mid-day changes (job cancellations, truck breakdowns)
- Deterministic mock data seeded by date for reproducible demos

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/optimize` | Run full VRP optimization |
| POST | `/api/reoptimize` | Re-optimize with changes |
| GET | `/api/fleet?region=` | Fleet status |
| GET | `/api/jobs?date=&region=` | Job queue |
| GET | `/api/routes?date=&region=` | Cached results |
| GET | `/api/stats?date=&region=` | Summary KPIs |
| GET | `/health` | Health check |
