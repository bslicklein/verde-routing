"use client";

import { useState } from "react";
import RouteMap from "@/components/Map";
import RouteDetails from "@/components/Sidebar/RouteDetails";
import FleetPanel from "@/components/Sidebar/FleetPanel";
import JobQueue from "@/components/Sidebar/JobQueue";
import OptimizeButton from "@/components/Controls/OptimizeButton";
import RegionSelector from "@/components/Controls/RegionSelector";
import StatsBar from "@/components/Controls/StatsBar";
import ReoptimizeModal from "@/components/ReoptimizeModal";
import OnboardingModal from "@/components/OnboardingModal";
import { useRouteStore } from "@/stores/routeStore";

type Tab = "routes" | "fleet" | "jobs";

export default function Home() {
  const [activeTab, setActiveTab] = useState<Tab>("routes");
  const [reoptimizeOpen, setReoptimizeOpen] = useState(false);
  const { comparison, error, date, setDate } = useRouteStore();

  const tabs: { id: Tab; label: string }[] = [
    { id: "routes", label: "Routes" },
    { id: "fleet", label: "Fleet" },
    { id: "jobs", label: "Jobs" },
  ];

  return (
    <div className="flex h-screen flex-col">
      {/* Top bar */}
      <header className="flex items-center justify-between border-b border-white/10 bg-slate-900 px-4 py-2.5">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-600 text-sm font-bold">
              V
            </div>
            <span className="text-lg font-bold tracking-tight">
              Verde Routing
            </span>
          </div>
          <RegionSelector />
        </div>
        <div className="flex items-center gap-3">
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-white"
          />
          {comparison && (
            <button
              onClick={() => setReoptimizeOpen(true)}
              className="rounded-lg border border-white/10 px-3 py-2 text-sm text-slate-300 hover:bg-white/5"
            >
              Re-Optimize
            </button>
          )}
          <OptimizeButton />
        </div>
      </header>

      {/* Error banner */}
      {error && (
        <div className="bg-red-500/10 px-4 py-2 text-sm text-red-400 border-b border-red-500/20">
          {error}
        </div>
      )}

      {/* Main content: map + sidebar */}
      <div className="flex flex-1 overflow-hidden">
        {/* Map area */}
        <div className="relative flex-1">
          <RouteMap />

          {/* Stats bar overlay at bottom of map */}
          {comparison && (
            <div className="absolute bottom-4 left-4 right-4 z-[1000]">
              <StatsBar />
            </div>
          )}
        </div>

        {/* Sidebar */}
        <aside className="flex w-[380px] flex-col border-l border-white/10 bg-slate-900/80">
          {/* Tab bar */}
          <div className="flex border-b border-white/10">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-4 py-2.5 text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? "border-b-2 border-green-500 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab content */}
          <div className="flex-1 overflow-y-auto">
            {activeTab === "routes" && <RouteDetails />}
            {activeTab === "fleet" && <FleetPanel />}
            {activeTab === "jobs" && <JobQueue />}
          </div>
        </aside>
      </div>

      {/* Modals */}
      <ReoptimizeModal
        open={reoptimizeOpen}
        onClose={() => setReoptimizeOpen(false)}
      />
      <OnboardingModal />
    </div>
  );
}
