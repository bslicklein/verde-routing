"use client";

import { useState } from "react";
import { useRouteStore } from "@/stores/routeStore";
import { reoptimizeRoutes } from "@/lib/api";

type ChangeType = "cancel_job" | "truck_breakdown" | "none";

export default function ReoptimizeModal({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const { date, region, comparison, setComparison, setLoading, setError } =
    useRouteStore();
  const [changeType, setChangeType] = useState<ChangeType>("none");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [selectedVehicleId, setSelectedVehicleId] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!open) return null;

  const routes = comparison?.optimized.routes ?? [];
  const allJobIds = routes.flatMap((r) => r.stops.map((s) => s.job_id));
  const allVehicleIds = routes.map((r) => r.vehicle_id);

  const handleReoptimize = async () => {
    setSubmitting(true);
    setLoading(true);
    try {
      const params: {
        date: string;
        region: typeof region;
        cancelled_job_ids?: string[];
        unavailable_vehicle_ids?: string[];
      } = { date, region };

      if (changeType === "cancel_job" && selectedJobId) {
        params.cancelled_job_ids = [selectedJobId];
      }
      if (changeType === "truck_breakdown" && selectedVehicleId) {
        params.unavailable_vehicle_ids = [selectedVehicleId];
      }

      const result = await reoptimizeRoutes(params);
      setComparison(result);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Re-optimization failed");
    } finally {
      setSubmitting(false);
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-xl border border-white/10 bg-slate-900 p-6 shadow-2xl">
        <h2 className="mb-4 text-lg font-bold text-white">
          Re-Optimize Routes
        </h2>

        <div className="mb-4 space-y-3">
          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="changeType"
              checked={changeType === "cancel_job"}
              onChange={() => setChangeType("cancel_job")}
              className="accent-green-500"
            />
            <span className="text-sm text-slate-300">Job Cancelled</span>
          </label>
          {changeType === "cancel_job" && (
            <select
              value={selectedJobId}
              onChange={(e) => setSelectedJobId(e.target.value)}
              className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
            >
              <option value="">Select a job...</option>
              {allJobIds.map((id) => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          )}

          <label className="flex items-center gap-2">
            <input
              type="radio"
              name="changeType"
              checked={changeType === "truck_breakdown"}
              onChange={() => setChangeType("truck_breakdown")}
              className="accent-green-500"
            />
            <span className="text-sm text-slate-300">Truck Breakdown</span>
          </label>
          {changeType === "truck_breakdown" && (
            <select
              value={selectedVehicleId}
              onChange={(e) => setSelectedVehicleId(e.target.value)}
              className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-white"
            >
              <option value="">Select a truck...</option>
              {allVehicleIds.map((id) => {
                const route = routes.find((r) => r.vehicle_id === id);
                return (
                  <option key={id} value={id}>
                    {route?.vehicle_name || id}
                  </option>
                );
              })}
            </select>
          )}
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 rounded-lg border border-white/10 px-4 py-2 text-sm text-slate-300 hover:bg-white/5"
          >
            Cancel
          </button>
          <button
            onClick={handleReoptimize}
            disabled={
              submitting ||
              changeType === "none" ||
              (changeType === "cancel_job" && !selectedJobId) ||
              (changeType === "truck_breakdown" && !selectedVehicleId)
            }
            className="flex-1 rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-500 disabled:opacity-50"
          >
            {submitting ? "Re-optimizing..." : "Re-Optimize"}
          </button>
        </div>
      </div>
    </div>
  );
}
