"""Distance matrix computation via OSRM with Haversine fallback."""

import math
import logging

import httpx

logger = logging.getLogger(__name__)

OSRM_BASE = "https://router.project-osrm.org"
EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine distance between two points in km."""
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def _haversine_matrix(locations: list[tuple[float, float]]) -> tuple[list[list[float]], list[list[float]]]:
    """Build distance (km) and duration (minutes) matrices using Haversine with road correction."""
    n = len(locations)
    dist_matrix = [[0.0] * n for _ in range(n)]
    dur_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = haversine_km(locations[i][0], locations[i][1],
                             locations[j][0], locations[j][1])
            road_d = d * 1.4  # road correction factor
            dist_matrix[i][j] = road_d
            dur_matrix[i][j] = (road_d / 40.0) * 60.0  # 40 km/h avg -> minutes

    return dist_matrix, dur_matrix


async def build_distance_matrix(
    locations: list[tuple[float, float]],
) -> tuple[list[list[float]], list[list[float]]]:
    """Build distance (km) and duration (minutes) matrices.

    Tries OSRM first, falls back to Haversine.
    locations: list of (lat, lng) tuples. First element is the depot.
    """
    n = len(locations)
    if n > 100:
        logger.warning("Too many locations (%d) for OSRM, using Haversine", n)
        return _haversine_matrix(locations)

    # OSRM expects lng,lat format
    coords = ";".join(f"{lng},{lat}" for lat, lng in locations)
    url = f"{OSRM_BASE}/table/v1/driving/{coords}"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, params={
                "annotations": "distance,duration",
            })
            resp.raise_for_status()
            data = resp.json()

        if data.get("code") != "Ok":
            logger.warning("OSRM returned %s, falling back to Haversine", data.get("code"))
            return _haversine_matrix(locations)

        # OSRM returns distances in meters and durations in seconds
        raw_dist = data["distances"]
        raw_dur = data["durations"]

        dist_matrix = [[0.0] * n for _ in range(n)]
        dur_matrix = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = (raw_dist[i][j] or 0) / 1000.0  # m -> km
                dur_matrix[i][j] = (raw_dur[i][j] or 0) / 60.0       # s -> min

        return dist_matrix, dur_matrix

    except Exception as e:
        logger.warning("OSRM failed (%s), using Haversine fallback", e)
        return _haversine_matrix(locations)


async def get_route_geometry(
    locations: list[tuple[float, float]],
) -> list[list[float]]:
    """Get route polyline geometry from OSRM for a sequence of stops.

    Returns list of [lat, lng] pairs for drawing on a map.
    """
    if len(locations) < 2:
        return [[lat, lng] for lat, lng in locations]

    coords = ";".join(f"{lng},{lat}" for lat, lng in locations)
    url = f"{OSRM_BASE}/route/v1/driving/{coords}"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, params={
                "overview": "full",
                "geometries": "geojson",
            })
            resp.raise_for_status()
            data = resp.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            return [[lat, lng] for lat, lng in locations]

        # GeoJSON coordinates are [lng, lat], convert to [lat, lng]
        geojson_coords = data["routes"][0]["geometry"]["coordinates"]
        return [[c[1], c[0]] for c in geojson_coords]

    except Exception:
        return [[lat, lng] for lat, lng in locations]
