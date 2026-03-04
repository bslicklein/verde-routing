import { create } from "zustand";
import type {
  ComparisonResult,
  Job,
  Region,
  RouteResult,
  Vehicle,
} from "@/types/vrp";

interface RouteState {
  // Data
  comparison: ComparisonResult | null;
  jobs: Job[];
  fleet: Vehicle[];

  // UI state
  region: Region;
  date: string;
  selectedRouteId: string | null;
  loading: boolean;
  error: string | null;

  // Actions
  setComparison: (c: ComparisonResult) => void;
  setJobs: (j: Job[]) => void;
  setFleet: (f: Vehicle[]) => void;
  setRegion: (r: Region) => void;
  setDate: (d: string) => void;
  selectRoute: (id: string | null) => void;
  setLoading: (l: boolean) => void;
  setError: (e: string | null) => void;
  reset: () => void;
}

const today = new Date().toISOString().split("T")[0];

export const useRouteStore = create<RouteState>((set) => ({
  comparison: null,
  jobs: [],
  fleet: [],
  region: "phoenix",
  date: today,
  selectedRouteId: null,
  loading: false,
  error: null,

  setComparison: (comparison) => set({ comparison, error: null }),
  setJobs: (jobs) => set({ jobs }),
  setFleet: (fleet) => set({ fleet }),
  setRegion: (region) => set({ region, comparison: null, selectedRouteId: null }),
  setDate: (date) => set({ date, comparison: null, selectedRouteId: null }),
  selectRoute: (selectedRouteId) => set({ selectedRouteId }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error, loading: false }),
  reset: () =>
    set({
      comparison: null,
      jobs: [],
      fleet: [],
      selectedRouteId: null,
      loading: false,
      error: null,
    }),
}));
