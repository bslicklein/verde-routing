const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

import type {
  ComparisonResult,
  Job,
  Region,
  Vehicle,
} from "@/types/vrp";

export async function optimizeRoutes(
  date: string,
  region: Region
): Promise<ComparisonResult> {
  return fetchAPI<ComparisonResult>("/api/optimize", {
    method: "POST",
    body: JSON.stringify({ date, region }),
  });
}

export async function reoptimizeRoutes(params: {
  date: string;
  region: Region;
  cancelled_job_ids?: string[];
  unavailable_vehicle_ids?: string[];
}): Promise<ComparisonResult> {
  return fetchAPI<ComparisonResult>("/api/reoptimize", {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export async function getFleet(region: Region): Promise<Vehicle[]> {
  return fetchAPI<Vehicle[]>(`/api/fleet?region=${region}`);
}

export async function getJobs(
  date: string,
  region: Region
): Promise<Job[]> {
  return fetchAPI<Job[]>(`/api/jobs?date=${date}&region=${region}`);
}
