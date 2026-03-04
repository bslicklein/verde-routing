"use client";

import { useEffect } from "react";
import { useRouteStore } from "@/stores/routeStore";
import { getFleet } from "@/lib/api";

const EQUIPMENT_LABELS: Record<string, string> = {
  standard: "Standard",
  ride_on: "Ride-On Mower",
  tree_service: "Tree Service",
  irrigation: "Irrigation",
  hardscape: "Hardscape",
};

const STATUS_STYLES: Record<string, { bg: string; text: string; label: string }> = {
  available: { bg: "bg-green-500/20", text: "text-green-400", label: "Available" },
  in_use: { bg: "bg-blue-500/20", text: "text-blue-400", label: "In Use" },
  out_of_service: { bg: "bg-red-500/20", text: "text-red-400", label: "Out of Service" },
};

export default function FleetPanel() {
  const fleet = useRouteStore((s) => s.fleet);
  const region = useRouteStore((s) => s.region);
  const setFleet = useRouteStore((s) => s.setFleet);

  useEffect(() => {
    getFleet(region).then(setFleet).catch(console.error);
  }, [region, setFleet]);

  return (
    <div className="space-y-2 p-3">
      {fleet.map((v) => {
        const st = STATUS_STYLES[v.status] || STATUS_STYLES.available;
        return (
          <div
            key={v.id}
            className="rounded-lg border border-white/10 bg-white/5 p-3"
          >
            <div className="mb-1.5 flex items-center justify-between">
              <span className="text-sm font-semibold text-white">
                {v.name}
              </span>
              <span
                className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${st.bg} ${st.text}`}
              >
                {st.label}
              </span>
            </div>
            <div className="flex gap-3 text-xs text-slate-400">
              <span>Crew: {v.crew_size}</span>
              <span>
                {v.equipment
                  .map((e) => EQUIPMENT_LABELS[e] || e)
                  .join(", ")}
              </span>
            </div>
          </div>
        );
      })}
      {!fleet.length && (
        <div className="p-4 text-center text-sm text-slate-500">
          Loading fleet...
        </div>
      )}
    </div>
  );
}
