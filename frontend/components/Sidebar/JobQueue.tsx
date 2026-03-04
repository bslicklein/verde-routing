"use client";

import { useEffect } from "react";
import { useRouteStore } from "@/stores/routeStore";
import { getJobs } from "@/lib/api";
import type { Job, JobStatus } from "@/types/vrp";

const STATUS_STYLES: Record<
  JobStatus,
  { bg: string; text: string }
> = {
  pending: { bg: "bg-slate-500/20", text: "text-slate-400" },
  assigned: { bg: "bg-blue-500/20", text: "text-blue-400" },
  completed: { bg: "bg-green-500/20", text: "text-green-400" },
  skipped: { bg: "bg-red-500/20", text: "text-red-400" },
};

const PRIORITY_COLORS: Record<string, string> = {
  urgent: "text-red-400",
  high: "text-orange-400",
  normal: "text-slate-300",
  low: "text-slate-500",
};

function formatTimeRange(start: number, end: number): string {
  const fmt = (m: number) => {
    const h = Math.floor(m / 60);
    const min = m % 60;
    const ampm = h >= 12 ? "PM" : "AM";
    const hour = h > 12 ? h - 12 : h === 0 ? 12 : h;
    return `${hour}:${min.toString().padStart(2, "0")}${ampm}`;
  };
  return `${fmt(start)}-${fmt(end)}`;
}

export default function JobQueue() {
  const jobs = useRouteStore((s) => s.jobs);
  const region = useRouteStore((s) => s.region);
  const date = useRouteStore((s) => s.date);
  const setJobs = useRouteStore((s) => s.setJobs);
  const comparison = useRouteStore((s) => s.comparison);

  useEffect(() => {
    getJobs(date, region).then(setJobs).catch(console.error);
  }, [date, region, setJobs]);

  // Determine assigned status from optimization results
  const assignedIds = new Set<string>();
  const skippedIds = new Set<string>();
  if (comparison) {
    for (const route of comparison.optimized.routes) {
      for (const stop of route.stops) {
        assignedIds.add(stop.job_id);
      }
    }
    for (const job of comparison.optimized.unassigned_jobs) {
      skippedIds.add(job.id);
    }
  }

  const getStatus = (job: Job): JobStatus => {
    if (assignedIds.has(job.id)) return "assigned";
    if (skippedIds.has(job.id)) return "skipped";
    return "pending";
  };

  return (
    <div className="space-y-1.5 p-3">
      {jobs.map((job) => {
        const status = getStatus(job);
        const st = STATUS_STYLES[status];
        return (
          <div
            key={job.id}
            className="rounded-lg border border-white/10 bg-white/5 p-2.5"
          >
            <div className="mb-1 flex items-center justify-between">
              <span className="text-sm font-medium text-slate-200 truncate max-w-[180px]">
                {job.property_name}
              </span>
              <span
                className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${st.bg} ${st.text}`}
              >
                {status}
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <span className={PRIORITY_COLORS[job.priority]}>
                {job.priority === "urgent" ? "!!!" : job.priority === "high" ? "!!" : ""}
                {job.priority}
              </span>
              <span>{job.job_type.replace(/_/g, " ")}</span>
              <span>{job.duration_minutes}min</span>
              <span className="text-slate-500">
                {formatTimeRange(job.time_window_start, job.time_window_end)}
              </span>
            </div>
          </div>
        );
      })}
      {!jobs.length && (
        <div className="p-4 text-center text-sm text-slate-500">
          Loading jobs...
        </div>
      )}
    </div>
  );
}
