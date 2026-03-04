"use client";

import { useRouteStore } from "@/stores/routeStore";

function kmToMiles(km: number): string {
  return (km * 0.621371).toFixed(0);
}

function formatDuration(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  if (h === 0) return `${m}m`;
  return `${h}h ${m}m`;
}

export default function StatsBar() {
  const comparison = useRouteStore((s) => s.comparison);

  if (!comparison) return null;

  const { optimized, naive, distance_saved_pct, time_saved_pct } = comparison;

  const stats = [
    {
      label: "Vehicles",
      value: `${optimized.total_vehicles_used}`,
      sub: null,
    },
    {
      label: "Jobs",
      value: `${optimized.total_jobs_assigned}`,
      sub: optimized.unassigned_jobs.length
        ? `${optimized.unassigned_jobs.length} skipped`
        : null,
    },
    {
      label: "Total Miles",
      value: `${kmToMiles(optimized.total_distance_km)}`,
      sub: `vs ${kmToMiles(naive.total_distance_km)} naive`,
    },
    {
      label: "Drive Time",
      value: formatDuration(optimized.total_drive_minutes),
      sub: `vs ${formatDuration(naive.total_drive_minutes)} naive`,
    },
    {
      label: "Dist Saved",
      value: `${distance_saved_pct}%`,
      sub: null,
      highlight: true,
    },
    {
      label: "Time Saved",
      value: `${time_saved_pct}%`,
      sub: null,
      highlight: true,
    },
    {
      label: "Utilization",
      value: `${optimized.avg_utilization_pct}%`,
      sub: `vs ${naive.avg_utilization_pct}% naive`,
      highlight: optimized.avg_utilization_pct >= 85,
    },
    {
      label: "Solver",
      value: `${optimized.solver_time_seconds}s`,
      sub: null,
    },
  ];

  return (
    <div className="flex items-center gap-1 overflow-x-auto rounded-xl border border-white/10 bg-slate-900/95 px-3 py-2 backdrop-blur">
      {stats.map((stat, i) => (
        <div
          key={stat.label}
          className={`flex flex-col items-center px-3 ${
            i < stats.length - 1 ? "border-r border-white/10" : ""
          }`}
        >
          <span className="text-[10px] uppercase tracking-wider text-slate-500">
            {stat.label}
          </span>
          <span
            className={`text-sm font-bold ${
              stat.highlight ? "text-green-400" : "text-white"
            }`}
          >
            {stat.value}
          </span>
          {stat.sub && (
            <span className="text-[10px] text-slate-500">{stat.sub}</span>
          )}
        </div>
      ))}
    </div>
  );
}
