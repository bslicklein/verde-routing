"""Routes endpoints - get cached optimization results."""

from fastapi import APIRouter, Query, HTTPException

from solver.models import OptimizationResult, Region

router = APIRouter()

# Shared cache reference - imported from optimize module
from routes.optimize import _cache, _cache_key


@router.get("/routes", response_model=OptimizationResult | None)
async def get_routes(
    date: str = Query(...),
    region: Region = Query(default=Region.phoenix),
):
    key = _cache_key(date, region.value)
    result = _cache.get(key)
    if not result:
        raise HTTPException(status_code=404, detail="No optimization results found. Run /api/optimize first.")
    return result
