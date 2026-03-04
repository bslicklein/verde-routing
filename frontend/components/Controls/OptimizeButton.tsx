"use client";

import { useRouteStore } from "@/stores/routeStore";
import { optimizeRoutes } from "@/lib/api";

export default function OptimizeButton() {
  const { date, region, loading, setLoading, setComparison, setError } =
    useRouteStore();

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const result = await optimizeRoutes(date, region);
      setComparison(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Optimization failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleOptimize}
      disabled={loading}
      className="flex items-center gap-2 rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white shadow-lg transition-all hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {loading ? (
        <>
          <svg
            className="h-4 w-4 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
          Optimizing...
        </>
      ) : (
        <>
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Optimize Routes
        </>
      )}
    </button>
  );
}
