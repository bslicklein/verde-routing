"use client";

import dynamic from "next/dynamic";

const RouteMap = dynamic(() => import("./RouteMap"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full w-full items-center justify-center bg-slate-900">
      <div className="text-slate-400">Loading map...</div>
    </div>
  ),
});

export default RouteMap;
