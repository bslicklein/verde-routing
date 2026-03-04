"""Verde Truck Routing Optimization - FastAPI Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import optimize, fleet, jobs, routes

app = FastAPI(
    title="Verde Routing Optimization",
    description="AI-powered truck routing for landscaping operations",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount route modules
app.include_router(optimize.router, prefix="/api")
app.include_router(fleet.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(routes.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "verde-routing"}


@app.get("/api/stats")
async def get_stats(date: str, region: str = "phoenix"):
    """Summary KPIs for a date/region."""
    from routes.optimize import _cache, _cache_key
    from data.job_generator import generate_jobs
    from data.mock_data import get_vehicles, get_depot
    from solver.models import Region, StatsResponse
    from solver.distance_matrix import build_distance_matrix
    from solver.vrp_solver import compute_naive_routing

    r = Region(region)
    key = _cache_key(date, region)
    cached = _cache.get(key)

    all_jobs = generate_jobs(date, r)
    all_vehicles = get_vehicles(r)
    depot = get_depot(r)

    # Get naive stats
    locations = [(depot.location.lat, depot.location.lng)]
    for job in all_jobs:
        locations.append((job.location.lat, job.location.lng))

    dist_matrix, dur_matrix = await build_distance_matrix(locations)
    naive_dist, naive_drive, naive_util = compute_naive_routing(
        all_jobs, all_vehicles, depot, dist_matrix, dur_matrix
    )

    if cached:
        dist_saved = (
            ((naive_dist - cached.total_distance_km) / naive_dist * 100)
            if naive_dist > 0 else 0
        )
        time_saved = (
            ((naive_drive - cached.total_drive_minutes) / naive_drive * 100)
            if naive_drive > 0 else 0
        )
        return StatsResponse(
            total_vehicles=len(all_vehicles),
            vehicles_used=cached.total_vehicles_used,
            total_jobs=len(all_jobs),
            jobs_assigned=cached.total_jobs_assigned,
            jobs_skipped=len(cached.unassigned_jobs),
            total_distance_km=cached.total_distance_km,
            total_drive_minutes=cached.total_drive_minutes,
            total_service_minutes=cached.total_service_minutes,
            avg_utilization_pct=cached.avg_utilization_pct,
            naive_distance_km=naive_dist,
            naive_drive_minutes=naive_drive,
            distance_saved_pct=round(max(0, dist_saved), 1),
            time_saved_pct=round(max(0, time_saved), 1),
        )

    return StatsResponse(
        total_vehicles=len(all_vehicles),
        vehicles_used=0,
        total_jobs=len(all_jobs),
        jobs_assigned=0,
        jobs_skipped=0,
        total_distance_km=0,
        total_drive_minutes=0,
        total_service_minutes=0,
        avg_utilization_pct=0,
        naive_distance_km=naive_dist,
        naive_drive_minutes=naive_drive,
        distance_saved_pct=0,
        time_saved_pct=0,
    )
