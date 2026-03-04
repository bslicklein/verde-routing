export type Region = "phoenix" | "san_diego";

export type EquipmentType =
  | "standard"
  | "ride_on"
  | "tree_service"
  | "irrigation"
  | "hardscape";

export type JobType =
  | "mow_and_blow"
  | "full_service"
  | "tree_trimming"
  | "irrigation_repair"
  | "hardscape_install"
  | "seasonal_cleanup"
  | "fertilization";

export type JobPriority = "low" | "normal" | "high" | "urgent";
export type JobStatus = "pending" | "assigned" | "completed" | "skipped";
export type VehicleStatus = "available" | "in_use" | "out_of_service";

export interface Location {
  lat: number;
  lng: number;
}

export interface Job {
  id: string;
  property_id: string;
  property_name: string;
  location: Location;
  job_type: JobType;
  priority: JobPriority;
  status: JobStatus;
  duration_minutes: number;
  crew_required: number;
  equipment_required: EquipmentType;
  time_window_start: number;
  time_window_end: number;
  region: Region;
}

export interface Vehicle {
  id: string;
  name: string;
  crew_size: number;
  equipment: EquipmentType[];
  status: VehicleStatus;
  region: Region;
  depot_id: string;
}

export interface StopResult {
  job_id: string;
  property_name: string;
  location: Location;
  arrival_minutes: number;
  departure_minutes: number;
  service_duration: number;
  drive_time_from_prev: number;
  distance_from_prev_km: number;
}

export interface RouteResult {
  vehicle_id: string;
  vehicle_name: string;
  color: string;
  stops: StopResult[];
  total_distance_km: number;
  total_drive_minutes: number;
  total_service_minutes: number;
  utilization_pct: number;
  route_geometry: [number, number][];
}

export interface OptimizationResult {
  date: string;
  region: Region;
  routes: RouteResult[];
  unassigned_jobs: Job[];
  total_vehicles_used: number;
  total_jobs_assigned: number;
  total_distance_km: number;
  total_drive_minutes: number;
  total_service_minutes: number;
  avg_utilization_pct: number;
  solver_time_seconds: number;
}

export interface NaiveResult {
  total_distance_km: number;
  total_drive_minutes: number;
  avg_utilization_pct: number;
}

export interface ComparisonResult {
  optimized: OptimizationResult;
  naive: NaiveResult;
  distance_saved_pct: number;
  time_saved_pct: number;
}

export interface StatsResponse {
  total_vehicles: number;
  vehicles_used: number;
  total_jobs: number;
  jobs_assigned: number;
  jobs_skipped: number;
  total_distance_km: number;
  total_drive_minutes: number;
  total_service_minutes: number;
  avg_utilization_pct: number;
  naive_distance_km: number;
  naive_drive_minutes: number;
  distance_saved_pct: number;
  time_saved_pct: number;
}
