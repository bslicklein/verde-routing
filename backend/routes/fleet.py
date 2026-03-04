"""Fleet endpoints."""

from fastapi import APIRouter, Query

from data.mock_data import get_vehicles
from solver.models import Region, Vehicle

router = APIRouter()


@router.get("/fleet", response_model=list[Vehicle])
async def get_fleet(region: Region = Query(default=Region.phoenix)):
    return get_vehicles(region)
