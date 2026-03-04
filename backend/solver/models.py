from __future__ import annotations

from enum import Enum
from pydantic import BaseModel


class Region(str, Enum):
    phoenix = "phoenix"
    san_diego = "san_diego"


class EquipmentType(str, Enum):
    standard = "standard"
    ride_on = "ride_on"
    tree_service = "tree_service"
    irrigation = "irrigation"
    hardscape = "hardscape"


class JobType(str, Enum):
    mow_and_blow = "mow_and_blow"
    full_service = "full_service"
    tree_trimming = "tree_trimming"
    irrigation_repair = "irrigation_repair"
    hardscape_install = "hardscape_install"
    seasonal_cleanup = "seasonal_cleanup"
    fertilization = "fertilization"


class JobPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class JobStatus(str, Enum):
    pending = "pending"
    assigned = "assigned"
    completed = "completed"
    skipped = "skipped"


class VehicleStatus(str, Enum):
    available = "available"
    in_use = "in_use"
    out_of_service = "out_of_service"


class PropertyType(str, Enum):
    hoa = "hoa"
    commercial = "commercial"
    medical = "medical"
    retail = "retail"
    industrial = "industrial"
    municipal = "municipal"
    residential_estate = "residential_estate"


# ── Core Models ──


class Location(BaseModel):
    lat: float
    lng: float


class Property(BaseModel):
    id: str
    name: str
    address: str
    location: Location
    property_type: PropertyType
    lot_acres: float
    region: Region


class Depot(BaseModel):
    id: str
    name: str
    location: Location
    region: Region


class Vehicle(BaseModel):
    id: str
    name: str
    crew_size: int
    equipment: list[EquipmentType]
    status: VehicleStatus
    region: Region
    depot_id: str


class Job(BaseModel):
    id: str
    property_id: str
    property_name: str
    location: Location
    job_type: JobType
    priority: JobPriority
    status: JobStatus = JobStatus.pending
    duration_minutes: int
    crew_required: int
    equipment_required: EquipmentType
    time_window_start: int  # minutes from midnight
    time_window_end: int  # minutes from midnight
    region: Region


# ── API Request/Response Models ──


class OptimizationRequest(BaseModel):
    date: str
    region: Region


class ReoptimizeRequest(BaseModel):
    date: str
    region: Region
    cancelled_job_ids: list[str] = []
    unavailable_vehicle_ids: list[str] = []
    new_jobs: list[Job] = []


class StopResult(BaseModel):
    job_id: str
    property_name: str
    location: Location
    arrival_minutes: int  # minutes from midnight
    departure_minutes: int
    service_duration: int
    drive_time_from_prev: int
    distance_from_prev_km: float


class RouteResult(BaseModel):
    vehicle_id: str
    vehicle_name: str
    color: str
    stops: list[StopResult]
    total_distance_km: float
    total_drive_minutes: int
    total_service_minutes: int
    utilization_pct: float
    route_geometry: list[list[float]]  # [[lat, lng], ...] for polylines


class OptimizationResult(BaseModel):
    date: str
    region: Region
    routes: list[RouteResult]
    unassigned_jobs: list[Job]
    total_vehicles_used: int
    total_jobs_assigned: int
    total_distance_km: float
    total_drive_minutes: int
    total_service_minutes: int
    avg_utilization_pct: float
    solver_time_seconds: float


class NaiveResult(BaseModel):
    total_distance_km: float
    total_drive_minutes: int
    avg_utilization_pct: float


class ComparisonResult(BaseModel):
    optimized: OptimizationResult
    naive: NaiveResult
    distance_saved_pct: float
    time_saved_pct: float


class StatsResponse(BaseModel):
    total_vehicles: int
    vehicles_used: int
    total_jobs: int
    jobs_assigned: int
    jobs_skipped: int
    total_distance_km: float
    total_drive_minutes: int
    total_service_minutes: int
    avg_utilization_pct: float
    naive_distance_km: float
    naive_drive_minutes: int
    distance_saved_pct: float
    time_saved_pct: float
