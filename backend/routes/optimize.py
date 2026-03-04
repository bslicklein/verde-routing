"""Optimization endpoints."""

from fastapi import APIRouter

from data.job_generator import generate_jobs
from data.mock_data import get_depot, get_vehicles
from solver.distance_matrix import build_distance_matrix
from solver.models import (
    ComparisonResult,
    NaiveResult,
    OptimizationRequest,
    OptimizationResult,
    ReoptimizeRequest,
)
from solver.vrp_solver import compute_naive_routing, solve_vrp

router = APIRouter()

# In-memory cache for results
_cache: dict[str, OptimizationResult] = {}


def _cache_key(date: str, region: str) -> str:
    return f"{date}:{region}"


@router.post("/optimize", response_model=ComparisonResult)
async def optimize_routes(req: OptimizationRequest):
    """Run full VRP optimization for a date + region."""
    jobs = generate_jobs(req.date, req.region)
    vehicles = get_vehicles(req.region)
    depot = get_depot(req.region)

    result = await solve_vrp(jobs, vehicles, depot, req.region, req.date)
    _cache[_cache_key(req.date, req.region.value)] = result

    # Compute naive routing for comparison
    locations = [(depot.location.lat, depot.location.lng)]
    for job in jobs:
        locations.append((job.location.lat, job.location.lng))

    dist_matrix, dur_matrix = await build_distance_matrix(locations)
    naive_dist, naive_drive, naive_util = compute_naive_routing(
        jobs, vehicles, depot, dist_matrix, dur_matrix
    )

    dist_saved = (
        ((naive_dist - result.total_distance_km) / naive_dist * 100)
        if naive_dist > 0 else 0
    )
    time_saved = (
        ((naive_drive - result.total_drive_minutes) / naive_drive * 100)
        if naive_drive > 0 else 0
    )

    return ComparisonResult(
        optimized=result,
        naive=NaiveResult(
            total_distance_km=naive_dist,
            total_drive_minutes=naive_drive,
            avg_utilization_pct=naive_util,
        ),
        distance_saved_pct=round(max(0, dist_saved), 1),
        time_saved_pct=round(max(0, time_saved), 1),
    )


@router.post("/reoptimize", response_model=ComparisonResult)
async def reoptimize_routes(req: ReoptimizeRequest):
    """Re-optimize with changes (cancellations, breakdowns, new jobs)."""
    jobs = generate_jobs(req.date, req.region)

    # Remove cancelled jobs
    if req.cancelled_job_ids:
        jobs = [j for j in jobs if j.id not in req.cancelled_job_ids]

    # Add new jobs
    jobs.extend(req.new_jobs)

    vehicles = get_vehicles(req.region)

    # Mark unavailable vehicles
    for v in vehicles:
        if v.id in req.unavailable_vehicle_ids:
            from solver.models import VehicleStatus
            v.status = VehicleStatus.out_of_service

    depot = get_depot(req.region)

    result = await solve_vrp(jobs, vehicles, depot, req.region, req.date)
    _cache[_cache_key(req.date, req.region.value)] = result

    # Naive comparison
    available_jobs = [j for j in jobs]
    locations = [(depot.location.lat, depot.location.lng)]
    for job in available_jobs:
        locations.append((job.location.lat, job.location.lng))

    dist_matrix, dur_matrix = await build_distance_matrix(locations)
    naive_dist, naive_drive, naive_util = compute_naive_routing(
        available_jobs, vehicles, depot, dist_matrix, dur_matrix
    )

    dist_saved = (
        ((naive_dist - result.total_distance_km) / naive_dist * 100)
        if naive_dist > 0 else 0
    )
    time_saved = (
        ((naive_drive - result.total_drive_minutes) / naive_drive * 100)
        if naive_drive > 0 else 0
    )

    return ComparisonResult(
        optimized=result,
        naive=NaiveResult(
            total_distance_km=naive_dist,
            total_drive_minutes=naive_drive,
            avg_utilization_pct=naive_util,
        ),
        distance_saved_pct=round(max(0, dist_saved), 1),
        time_saved_pct=round(max(0, time_saved), 1),
    )
