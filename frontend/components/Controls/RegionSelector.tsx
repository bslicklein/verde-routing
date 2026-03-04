"use client";

import { useRouteStore } from "@/stores/routeStore";
import type { Region } from "@/types/vrp";

const REGIONS: { value: Region; label: string }[] = [
  { value: "phoenix", label: "Phoenix" },
  { value: "san_diego", label: "San Diego" },
];

export default function RegionSelector() {
  const region = useRouteStore((s) => s.region);
  const setRegion = useRouteStore((s) => s.setRegion);

  return (
    <div className="flex rounded-lg bg-white/10 p-0.5">
      {REGIONS.map((r) => (
        <button
          key={r.value}
          onClick={() => setRegion(r.value)}
          className={`rounded-md px-3 py-1.5 text-sm font-medium transition-all ${
            region === r.value
              ? "bg-white/20 text-white shadow"
              : "text-slate-400 hover:text-white"
          }`}
        >
          {r.label}
        </button>
      ))}
    </div>
  );
}
