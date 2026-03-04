"""Google OR-Tools CVRPTW solver for Verde routing."""

import logging
import time

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from solver.distance_matrix import build_distance_matrix, get_route_geometry
from solver.models import (
    Depot,
    Job,
    Location,
    OptimizationResult,
    RouteResult,
    StopResult,
    Vehicle,
    Region,
)

logger = logging.getLogger(__name__)

# 15 distinct colors for route visualization
ROUTE_COLORS = [
    "#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed",
    "#0891b2", "#e11d48", "#4f46e5", "#059669", "#ca8a04",
    "#9333ea", "#0d9488", "#f97316", "#6366f1", "#84cc16",
]

WORKDAY_START = 360   # 6:00 AM in minutes
WORKDAY_END = 1080    # 6:00 PM in minutes
MAX_SOLVER_TIME = 15  # seconds


async def solve_vrp(
    jobs: list[Job],
    vehicles: list[Vehicle],
    depot: Depot,
    region: Region,
    date_str: str,
) -> OptimizationResult:
    """Run OR-Tools CVRPTW solver and return optimized routes."""
    start_time = time.time()

    available_vehicles = [v for v in vehicles if v.status.value == "available"]

    if not jobs or not available_vehicles:
        return OptimizationResult(
            date=date_str,
            region=region,
            routes=[],
            unassigned_jobs=jobs,
            total_vehicles_used=0,
            total_jobs_assigned=0,
            total_distance_km=0,
            total_drive_minutes=0,
            total_service_minutes=0,
            avg_utilization_pct=0,
            solver_time_seconds=time.time() - start_time,
        )

    num_vehicles = len(available_vehicles)
    num_jobs = len(jobs)

    # Build location list: depot first, then all jobs
    locations: list[tuple[float, float]] = [
        (depot.location.lat, depot.location.lng)
    ]
    for job in jobs:
        locations.append((job.location.lat, job.location.lng))

    # Get distance and duration matrices
    dist_matrix_km, dur_matrix_min = await build_distance_matrix(locations)

    # Convert to integer matrices (OR-Tools needs ints)
    # Use meters for distance, seconds for time
    dist_matrix_int = [
        [int(d * 1000) for d in row] for row in dist_matrix_km
    ]
    dur_matrix_int = [
        [int(d * 60) for d in row] for row in dur_matrix_min
    ]

    # Create routing index manager
    # All vehicles start and end at depot (index 0)
    manager = pywrapcp.RoutingIndexManager(
        len(locations), num_vehicles, 0
    )
    routing = pywrapcp.RoutingModel(manager)

    # ── Distance callback ──
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return dist_matrix_int[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # ── Time dimension ──
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        travel = dur_matrix_int[from_node][to_node]
        # Add service time at the from_node (except depot)
        service = 0
        if from_node > 0:
            service = jobs[from_node - 1].duration_minutes * 60  # to seconds
        return travel + service

    time_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.AddDimensionWithVehicleCapacity(
        time_callback_index,
        30 * 60,  # 30 min slack (allow waiting)
        [WORKDAY_END * 60] * num_vehicles,  # max time per vehicle (in seconds)
        False,  # don't fix start cumul to zero - we set time windows
        "Time",
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    # Set time windows for each job
    for job_idx, job in enumerate(jobs):
        node_index = manager.NodeToIndex(job_idx + 1)
        time_dimension.CumulVar(node_index).SetRange(
            job.time_window_start * 60,  # to seconds
            job.time_window_end * 60,
        )

    # Depot time window
    for v in range(num_vehicles):
        start_index = routing.Start(v)
        time_dimension.CumulVar(start_index).SetRange(
            WORKDAY_START * 60,
            WORKDAY_END * 60,
        )
        end_index = routing.End(v)
        time_dimension.CumulVar(end_index).SetRange(
            WORKDAY_START * 60,
            WORKDAY_END * 60,
        )

    # ── Equipment constraints ──
    # Use VehicleVar to restrict which vehicles can serve each job
    solver = routing.solver()
    for job_idx, job in enumerate(jobs):
        node_index = manager.NodeToIndex(job_idx + 1)
        allowed: list[int] = []
        for v_idx, vehicle in enumerate(available_vehicles):
            if job.equipment_required in vehicle.equipment:
                if vehicle.crew_size >= job.crew_required:
                    allowed.append(int(v_idx))
        if allowed and len(allowed) < num_vehicles:
            vehicle_var = routing.VehicleVar(node_index)
            # Add allowed vehicles + -1 (unperformed)
            allowed_with_unperformed = allowed + [-1]
            solver.Add(vehicle_var.Member(allowed_with_unperformed))

    # ── Allow dropping jobs with penalty ──
    penalty = 100_000_000  # high penalty for dropping
    for job_idx in range(num_jobs):
        node_index = manager.NodeToIndex(job_idx + 1)
        routing.AddDisjunction([node_index], penalty)

    # ── Search parameters ──
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.seconds = MAX_SOLVER_TIME

    # ── Solve ──
    solution = routing.SolveWithParameters(search_params)

    if not solution:
        return OptimizationResult(
            date=date_str,
            region=region,
            routes=[],
            unassigned_jobs=jobs,
            total_vehicles_used=0,
            total_jobs_assigned=0,
            total_distance_km=0,
            total_drive_minutes=0,
            total_service_minutes=0,
            avg_utilization_pct=0,
            solver_time_seconds=time.time() - start_time,
        )

    # ── Extract solution ──
    routes: list[RouteResult] = []
    assigned_job_ids: set[str] = set()
    total_dist = 0.0
    total_drive = 0
    total_service = 0

    for v_idx in range(num_vehicles):
        vehicle = available_vehicles[v_idx]
        index = routing.Start(v_idx)
        stops: list[StopResult] = []
        route_locations: list[tuple[float, float]] = [
            (depot.location.lat, depot.location.lng)
        ]
        route_dist = 0.0
        route_drive = 0
        route_service = 0
        prev_node = 0

        while not routing.IsEnd(index):
            next_index = solution.Value(routing.NextVar(index))
            node = manager.IndexToNode(next_index)

            if not routing.IsEnd(next_index) and node > 0:
                job = jobs[node - 1]
                arrival_sec = solution.Value(time_dimension.CumulVar(next_index))
                arrival_min = arrival_sec // 60
                drive_from_prev = dur_matrix_min[prev_node][node]
                dist_from_prev = dist_matrix_km[prev_node][node]

                stops.append(StopResult(
                    job_id=job.id,
                    property_name=job.property_name,
                    location=job.location,
                    arrival_minutes=int(arrival_min),
                    departure_minutes=int(arrival_min + job.duration_minutes),
                    service_duration=job.duration_minutes,
                    drive_time_from_prev=int(drive_from_prev),
                    distance_from_prev_km=round(dist_from_prev, 2),
                ))

                route_locations.append((job.location.lat, job.location.lng))
                route_dist += dist_from_prev
                route_drive += int(drive_from_prev)
                route_service += job.duration_minutes
                assigned_job_ids.add(job.id)
                prev_node = node

            index = next_index

        if stops:
            # Add return to depot
            last_node = manager.IndexToNode(
                solution.Value(routing.NextVar(
                    routing.Start(v_idx)
                ))
            )
            # Walk to find the actual last job node
            temp_idx = routing.Start(v_idx)
            last_job_node = 0
            while not routing.IsEnd(temp_idx):
                n = manager.IndexToNode(temp_idx)
                if n > 0:
                    last_job_node = n
                temp_idx = solution.Value(routing.NextVar(temp_idx))

            if last_job_node > 0:
                route_dist += dist_matrix_km[last_job_node][0]
                route_drive += int(dur_matrix_min[last_job_node][0])
                route_locations.append((depot.location.lat, depot.location.lng))

            # Get route geometry
            geometry = await get_route_geometry(route_locations)

            total_work = route_drive + route_service
            available_minutes = WORKDAY_END - WORKDAY_START
            utilization = min(100.0, (total_work / available_minutes) * 100) if available_minutes > 0 else 0

            routes.append(RouteResult(
                vehicle_id=vehicle.id,
                vehicle_name=vehicle.name,
                color=ROUTE_COLORS[v_idx % len(ROUTE_COLORS)],
                stops=stops,
                total_distance_km=round(route_dist, 2),
                total_drive_minutes=route_drive,
                total_service_minutes=route_service,
                utilization_pct=round(utilization, 1),
                route_geometry=geometry,
            ))

            total_dist += route_dist
            total_drive += route_drive
            total_service += route_service

    # Find unassigned jobs
    unassigned = [j for j in jobs if j.id not in assigned_job_ids]

    # Calculate average utilization
    active_routes = [r for r in routes if r.stops]
    avg_util = (
        sum(r.utilization_pct for r in active_routes) / len(active_routes)
        if active_routes else 0
    )

    return OptimizationResult(
        date=date_str,
        region=region,
        routes=[r for r in routes if r.stops],
        unassigned_jobs=unassigned,
        total_vehicles_used=len(active_routes),
        total_jobs_assigned=len(assigned_job_ids),
        total_distance_km=round(total_dist, 2),
        total_drive_minutes=total_drive,
        total_service_minutes=total_service,
        avg_utilization_pct=round(avg_util, 1),
        solver_time_seconds=round(time.time() - start_time, 2),
    )


def compute_naive_routing(
    jobs: list[Job],
    vehicles: list[Vehicle],
    depot: Depot,
    dist_matrix_km: list[list[float]],
    dur_matrix_min: list[list[float]],
) -> tuple[float, int, float]:
    """Compute naive nearest-available-truck routing for comparison.

    Returns (total_distance_km, total_drive_minutes, avg_utilization_pct).
    """
    available = [v for v in vehicles if v.status.value == "available"]
    if not available or not jobs:
        return 0.0, 0, 0.0

    # Assign jobs to trucks in order, each truck gets jobs greedily
    truck_jobs: dict[int, list[int]] = {i: [] for i in range(len(available))}
    truck_idx = 0
    for job_idx in range(len(jobs)):
        truck_jobs[truck_idx % len(available)].append(job_idx)
        truck_idx += 1

    total_dist = 0.0
    total_drive = 0
    utils = []

    for v_idx, job_indices in truck_jobs.items():
        if not job_indices:
            continue
        route_dist = 0.0
        route_drive = 0
        route_service = 0
        prev = 0  # depot

        for ji in job_indices:
            node = ji + 1
            route_dist += dist_matrix_km[prev][node]
            route_drive += int(dur_matrix_min[prev][node])
            route_service += jobs[ji].duration_minutes
            prev = node

        # Return to depot
        route_dist += dist_matrix_km[prev][0]
        route_drive += int(dur_matrix_min[prev][0])

        total_dist += route_dist
        total_drive += route_drive

        available_minutes = WORKDAY_END - WORKDAY_START
        util = min(100.0, ((route_drive + route_service) / available_minutes) * 100) if available_minutes > 0 else 0
        utils.append(util)

    avg_util = sum(utils) / len(utils) if utils else 0
    return round(total_dist, 2), total_drive, round(avg_util, 1)
