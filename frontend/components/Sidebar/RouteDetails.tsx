"use client";

import { useRouteStore } from "@/stores/routeStore";
import type { RouteResult } from "@/types/vrp";

function formatTime(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  const ampm = h >= 12 ? "PM" : "AM";
  const hour = h > 12 ? h - 12 : h === 0 ? 12 : h;
  return `${hour}:${m.toString().padStart(2, "0")} ${ampm}`;
}

function kmToMiles(km: number): string {
  return (km * 0.621371).toFixed(1);
}

function RouteCard({ route }: { route: RouteResult }) {
  const selectedRouteId = useRouteStore((s) => s.selectedRouteId);
  const selectRoute = useRouteStore((s) => s.selectRoute);
  const isSelected = selectedRouteId === route.vehicle_id;

  return (
    <div
      onClick={() => selectRoute(isSelected ? null : route.vehicle_id)}
      className={`cursor-pointer rounded-lg border p-3 transition-all ${
        isSelected
          ? "border-white/30 bg-white/10"
          : "border-white/10 bg-white/5 hover:bg-white/8"
      }`}
    >
      {/* Header */}
      <div className="mb-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div
            className="h-3 w-3 rounded-full"
            style={{ backgroundColor: route.color }}
          />
          <span className="text-sm font-semibold text-white">
            {route.vehicle_name}
          </span>
        </div>
        <span className="text-xs text-slate-400">
          {route.stops.length} stops
        </span>
      </div>

      {/* Metrics row */}
      <div className="flex gap-3 text-xs text-slate-300">
        <span>{kmToMiles(route.total_distance_km)} mi</span>
        <span>{route.total_drive_minutes} min drive</span>
        <span
          className={`font-medium ${
            route.utilization_pct >= 85
              ? "text-green-400"
              : route.utilization_pct >= 70
              ? "text-yellow-400"
              : "text-red-400"
          }`}
        >
          {route.utilization_pct}% util
        </span>
      </div>

      {/* Expanded stop list */}
      {isSelected && (
        <div className="mt-3 space-y-1.5 border-t border-white/10 pt-3">
          {route.stops.map((stop, idx) => (
            <div
              key={stop.job_id}
              className="flex items-start gap-2 text-xs"
            >
              <div
                className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold text-white"
                style={{ backgroundColor: route.color }}
              >
                {idx + 1}
              </div>
              <div className="min-w-0 flex-1">
                <div className="truncate font-medium text-slate-200">
                  {stop.property_name}
                </div>
                <div className="text-slate-400">
                  {formatTime(stop.arrival_minutes)} -{" "}
                  {formatTime(stop.departure_minutes)} |{" "}
                  {stop.service_duration}min service |{" "}
                  {stop.drive_time_from_prev}min drive
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function RouteDetails() {
  const comparison = useRouteStore((s) => s.comparison);
  const routes = comparison?.optimized.routes ?? [];

  if (!routes.length) {
    return (
      <div className="p-4 text-center text-sm text-slate-500">
        No routes yet. Click &quot;Optimize Routes&quot; to generate.
      </div>
    );
  }

  return (
    <div className="space-y-2 p-3">
      {routes.map((route) => (
        <RouteCard key={route.vehicle_id} route={route} />
      ))}
    </div>
  );
}
