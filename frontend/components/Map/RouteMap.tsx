"use client";

import { useEffect } from "react";
import L from "leaflet";
import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useRouteStore } from "@/stores/routeStore";

// Fix default marker icons
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)
  ._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

const DEPOT_LOCATIONS = {
  phoenix: { lat: 33.4373, lng: -111.9838 },
  san_diego: { lat: 32.8341, lng: -117.1447 },
};

function createNumberedIcon(number: number, color: string) {
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="
      background: ${color};
      color: white;
      border-radius: 50%;
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 700;
      border: 2px solid white;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
    ">${number}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

function createDepotIcon() {
  return L.divIcon({
    className: "depot-marker",
    html: `<div style="
      background: #1e293b;
      color: #22c55e;
      border-radius: 8px;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      border: 2px solid #22c55e;
      box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    ">&#9750;</div>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
  });
}

function createUnassignedIcon() {
  return L.divIcon({
    className: "unassigned-marker",
    html: `<div style="
      background: #6b7280;
      color: white;
      border-radius: 50%;
      width: 22px;
      height: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      border: 2px solid #ef4444;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    ">!</div>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11],
  });
}

function formatTime(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  const ampm = h >= 12 ? "PM" : "AM";
  const hour = h > 12 ? h - 12 : h === 0 ? 12 : h;
  return `${hour}:${m.toString().padStart(2, "0")} ${ampm}`;
}

function FitBounds() {
  const map = useMap();
  const comparison = useRouteStore((s) => s.comparison);
  const region = useRouteStore((s) => s.region);

  useEffect(() => {
    if (!comparison?.optimized.routes.length) {
      const depot = DEPOT_LOCATIONS[region];
      map.setView([depot.lat, depot.lng], 11);
      return;
    }

    const bounds: [number, number][] = [];
    const depot = DEPOT_LOCATIONS[region];
    bounds.push([depot.lat, depot.lng]);

    for (const route of comparison.optimized.routes) {
      for (const stop of route.stops) {
        bounds.push([stop.location.lat, stop.location.lng]);
      }
    }
    for (const job of comparison.optimized.unassigned_jobs) {
      bounds.push([job.location.lat, job.location.lng]);
    }

    if (bounds.length > 1) {
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }, [comparison, region, map]);

  return null;
}

export default function RouteMap() {
  const comparison = useRouteStore((s) => s.comparison);
  const region = useRouteStore((s) => s.region);
  const selectedRouteId = useRouteStore((s) => s.selectedRouteId);
  const selectRoute = useRouteStore((s) => s.selectRoute);

  const depot = DEPOT_LOCATIONS[region];
  const routes = comparison?.optimized.routes ?? [];
  const unassigned = comparison?.optimized.unassigned_jobs ?? [];

  return (
    <MapContainer
      center={[depot.lat, depot.lng]}
      zoom={11}
      className="h-full w-full"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <FitBounds />

      {/* Depot marker */}
      <Marker position={[depot.lat, depot.lng]} icon={createDepotIcon()}>
        <Popup>
          <strong>Verde Depot</strong>
          <br />
          {region === "phoenix" ? "Phoenix Yard" : "San Diego Yard"}
        </Popup>
      </Marker>

      {/* Route polylines */}
      {routes.map((route) => {
        const isSelected = selectedRouteId === route.vehicle_id;
        const isOther = selectedRouteId && !isSelected;
        return (
          <Polyline
            key={route.vehicle_id}
            positions={route.route_geometry as [number, number][]}
            pathOptions={{
              color: route.color,
              weight: isSelected ? 5 : isOther ? 2 : 3,
              opacity: isOther ? 0.25 : 0.85,
            }}
            eventHandlers={{
              click: () => selectRoute(route.vehicle_id),
            }}
          />
        );
      })}

      {/* Stop markers */}
      {routes.map((route) => {
        const isOther =
          selectedRouteId && selectedRouteId !== route.vehicle_id;
        if (isOther) return null;
        return route.stops.map((stop, idx) => (
          <Marker
            key={stop.job_id}
            position={[stop.location.lat, stop.location.lng]}
            icon={createNumberedIcon(idx + 1, route.color)}
          >
            <Popup>
              <div className="text-sm">
                <strong>
                  #{idx + 1} {stop.property_name}
                </strong>
                <br />
                Arrive: {formatTime(stop.arrival_minutes)}
                <br />
                Service: {stop.service_duration} min
                <br />
                Drive from prev: {stop.drive_time_from_prev} min (
                {stop.distance_from_prev_km} km)
              </div>
            </Popup>
          </Marker>
        ));
      })}

      {/* Unassigned job markers */}
      {unassigned.map((job) => (
        <Marker
          key={job.id}
          position={[job.location.lat, job.location.lng]}
          icon={createUnassignedIcon()}
        >
          <Popup>
            <div className="text-sm">
              <strong>{job.property_name}</strong>
              <br />
              <span className="text-red-600">Unassigned</span>
              <br />
              {job.job_type.replace(/_/g, " ")} - {job.duration_minutes} min
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
