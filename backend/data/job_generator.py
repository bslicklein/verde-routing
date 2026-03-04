"""Deterministic daily job generation from properties."""

import hashlib
import random

from data.mock_data import get_properties
from solver.models import (
    EquipmentType,
    Job,
    JobPriority,
    JobType,
    PropertyType,
    Region,
)

# Job types and their requirements
JOB_CONFIGS = {
    JobType.mow_and_blow: {
        "equipment": EquipmentType.standard,
        "crew": 2,
        "base_minutes": 45,
        "weight": 40,
    },
    JobType.full_service: {
        "equipment": EquipmentType.ride_on,
        "crew": 3,
        "base_minutes": 90,
        "weight": 25,
    },
    JobType.tree_trimming: {
        "equipment": EquipmentType.tree_service,
        "crew": 3,
        "base_minutes": 120,
        "weight": 8,
    },
    JobType.irrigation_repair: {
        "equipment": EquipmentType.irrigation,
        "crew": 1,
        "base_minutes": 60,
        "weight": 8,
    },
    JobType.hardscape_install: {
        "equipment": EquipmentType.hardscape,
        "crew": 4,
        "base_minutes": 180,
        "weight": 4,
    },
    JobType.seasonal_cleanup: {
        "equipment": EquipmentType.standard,
        "crew": 3,
        "base_minutes": 75,
        "weight": 10,
    },
    JobType.fertilization: {
        "equipment": EquipmentType.standard,
        "crew": 1,
        "base_minutes": 30,
        "weight": 5,
    },
}

# Time windows by property type (minutes from midnight)
TIME_WINDOWS = {
    PropertyType.medical: (360, 540),       # 6:00-9:00 AM (before patients)
    PropertyType.retail: (390, 600),         # 6:30-10:00 AM (before stores open)
    PropertyType.hoa: (420, 660),            # 7:00-11:00 AM (morning)
    PropertyType.commercial: (420, 720),     # 7:00-12:00 PM (flexible)
    PropertyType.industrial: (420, 780),     # 7:00-1:00 PM (very flexible)
    PropertyType.municipal: (420, 720),      # 7:00-12:00 PM
    PropertyType.residential_estate: (480, 720),  # 8:00-12:00 PM
}


def _seed_for_date(date_str: str, region: Region) -> int:
    """Create a deterministic seed from date + region."""
    h = hashlib.md5(f"{date_str}:{region.value}".encode()).hexdigest()
    return int(h[:8], 16)


def _pick_job_type(rng: random.Random) -> JobType:
    """Weighted random job type selection."""
    types = list(JOB_CONFIGS.keys())
    weights = [JOB_CONFIGS[t]["weight"] for t in types]
    return rng.choices(types, weights=weights, k=1)[0]


def generate_jobs(date_str: str, region: Region) -> list[Job]:
    """Generate deterministic jobs for a given date and region."""
    seed = _seed_for_date(date_str, region)
    rng = random.Random(seed)

    properties = get_properties(region)
    num_jobs = rng.randint(25, 35) if region == Region.phoenix else rng.randint(15, 25)

    # Shuffle properties and pick a subset (some properties may get multiple jobs)
    candidates = list(properties)
    rng.shuffle(candidates)

    jobs: list[Job] = []
    for i in range(num_jobs):
        prop = candidates[i % len(candidates)]
        job_type = _pick_job_type(rng)
        config = JOB_CONFIGS[job_type]

        # Scale duration by lot size
        lot_factor = max(0.5, min(2.0, prop.lot_acres / 8.0))
        duration = int(config["base_minutes"] * lot_factor)

        # Time windows from property type
        tw_start, tw_end = TIME_WINDOWS[prop.property_type]
        # Add some randomness to the window (shift by up to ±30 min)
        shift = rng.randint(-30, 30)
        tw_start = max(360, tw_start + shift)
        tw_end = min(1080, tw_end + shift)  # cap at 6 PM

        # Priority
        priority_roll = rng.random()
        if priority_roll < 0.05:
            priority = JobPriority.urgent
        elif priority_roll < 0.20:
            priority = JobPriority.high
        elif priority_roll < 0.80:
            priority = JobPriority.normal
        else:
            priority = JobPriority.low

        jobs.append(Job(
            id=f"{region.value[:3]}-job-{i+1:03d}",
            property_id=prop.id,
            property_name=prop.name,
            location=prop.location,
            job_type=job_type,
            priority=priority,
            duration_minutes=duration,
            crew_required=config["crew"],
            equipment_required=config["equipment"],
            time_window_start=tw_start,
            time_window_end=tw_end,
            region=region,
        ))

    return jobs
