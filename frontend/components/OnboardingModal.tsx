"use client";

import { useState, useEffect } from "react";

const STEPS = [
  {
    title: "Welcome to Verde Routing",
    description:
      "AI-powered route optimization for landscaping operations. This tool uses Google OR-Tools to find the most efficient truck routes, reducing drive time by 30-45% compared to manual dispatching.",
    icon: (
      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-green-600 text-2xl font-bold">
        V
      </div>
    ),
  },
  {
    title: "Choose a Region & Date",
    description:
      "Toggle between Phoenix and San Diego to see different service areas. Pick a date to generate that day's job list — each date produces a unique set of jobs so you can demo different scenarios.",
    icon: (
      <svg className="h-14 w-14 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l5.447 2.724A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
      </svg>
    ),
  },
  {
    title: "Optimize Routes",
    description:
      "Click the green \"Optimize Routes\" button to run the VRP solver. It builds a distance matrix using real road data, then finds optimal routes respecting time windows, equipment needs, and crew sizes. Takes about 15-20 seconds.",
    icon: (
      <svg className="h-14 w-14 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
  },
  {
    title: "Explore the Results",
    description:
      "Color-coded routes appear on the map with numbered stops. Click any route on the map or sidebar to isolate it and see the stop-by-stop breakdown with arrival times. The stats bar at the bottom shows distance and time savings vs naive routing.",
    icon: (
      <svg className="h-14 w-14 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
  {
    title: "Re-Optimize on the Fly",
    description:
      "Things change mid-day — a job gets cancelled or a truck breaks down. Click \"Re-Optimize\" to simulate a disruption and watch the solver reassign routes in real time. Check the Fleet and Jobs tabs for crew and job details.",
    icon: (
      <svg className="h-14 w-14 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
    ),
  },
];

const STORAGE_KEY = "verde-onboarding-seen";

export default function OnboardingModal() {
  const [open, setOpen] = useState(false);
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      setOpen(true);
    }
  }, []);

  const handleClose = () => {
    localStorage.setItem(STORAGE_KEY, "true");
    setOpen(false);
  };

  const handleNext = () => {
    if (step < STEPS.length - 1) {
      setStep(step + 1);
    } else {
      handleClose();
    }
  };

  const handleBack = () => {
    if (step > 0) setStep(step - 1);
  };

  if (!open) return null;

  const current = STEPS[step];
  const isLast = step === STEPS.length - 1;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-lg rounded-2xl border border-white/10 bg-slate-900 shadow-2xl">
        {/* Progress dots */}
        <div className="flex justify-center gap-1.5 pt-5">
          {STEPS.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 rounded-full transition-all ${
                i === step
                  ? "w-6 bg-green-500"
                  : i < step
                  ? "w-1.5 bg-green-500/50"
                  : "w-1.5 bg-white/15"
              }`}
            />
          ))}
        </div>

        {/* Content */}
        <div className="flex flex-col items-center px-8 pb-2 pt-6 text-center">
          <div className="mb-4">{current.icon}</div>
          <h2 className="mb-2 text-xl font-bold text-white">{current.title}</h2>
          <p className="text-sm leading-relaxed text-slate-400">
            {current.description}
          </p>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between px-8 pb-6 pt-4">
          <button
            onClick={handleClose}
            className="text-sm text-slate-500 hover:text-slate-300"
          >
            Skip
          </button>
          <div className="flex gap-2">
            {step > 0 && (
              <button
                onClick={handleBack}
                className="rounded-lg border border-white/10 px-4 py-2 text-sm text-slate-300 hover:bg-white/5"
              >
                Back
              </button>
            )}
            <button
              onClick={handleNext}
              className="rounded-lg bg-green-600 px-5 py-2 text-sm font-semibold text-white hover:bg-green-500"
            >
              {isLast ? "Get Started" : "Next"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
