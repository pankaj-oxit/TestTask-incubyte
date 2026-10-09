import type { ReactNode } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import * as employeesApi from "../api/employees";
import * as insightsApi from "../api/insights";
import InsightsPage from "../pages/InsightsPage";

function wrap(ui: ReactNode) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return (
    <QueryClientProvider client={client}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>
  );
}

describe("InsightsPage", () => {
  it("renders summary stat cards from API", async () => {
    vi.spyOn(insightsApi, "fetchInsightsSummary").mockResolvedValue({
      headcount: 100,
      average_salary_usd: 75000,
      median_salary_usd: 72000,
    });
    vi.spyOn(insightsApi, "fetchInsightsByCountry").mockResolvedValue([]);
    vi.spyOn(insightsApi, "fetchInsightsByJobTitle").mockResolvedValue([]);
    vi.spyOn(insightsApi, "fetchInsightsDistribution").mockResolvedValue({
      headcount: 0,
      buckets: Array.from({ length: 10 }, (_, i) => ({ range: `${i}`, count: 0 })),
    });
    vi.spyOn(employeesApi, "fetchMetaFilters").mockResolvedValue({
      countries: [],
      job_titles: [],
      departments: [],
    });

    render(wrap(<InsightsPage />));

    expect(await screen.findByText("Headcount")).toBeInTheDocument();
    expect(screen.getByText("100")).toBeInTheDocument();
    expect(screen.getByText(/department breakdown is on the roadmap/i)).toBeInTheDocument();
  });
});

