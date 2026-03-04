"""Job endpoints."""

from datetime import date

from fastapi import APIRouter, Query

from data.job_generator import generate_jobs
from solver.models import Job, Region

router = APIRouter()


@router.get("/jobs", response_model=list[Job])
async def get_jobs(
    date: str = Query(default=str(date.today())),
    region: Region = Query(default=Region.phoenix),
):
    return generate_jobs(date, region)
