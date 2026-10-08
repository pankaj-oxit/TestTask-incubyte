import type { ReactNode } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import * as employeesApi from "../api/employees";
import EmployeesPage from "../pages/EmployeesPage";

function wrap(ui: ReactNode) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return (
    <QueryClientProvider client={client}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>
  );
}

describe("EmployeesPage", () => {
  it("renders employee rows from list API", async () => {
    vi.spyOn(employeesApi, "listEmployees").mockResolvedValue({
      items: [
        {
          id: 1,
          employee_code: "EMP-000001",
          first_name: "Jane",
          last_name: "Doe",
          email: "jane@acme.example",
          job_title: "Engineer",
          department: "Engineering",
          country_code: "US",
          currency: "USD",
          annual_salary: 95000,
          hire_date: "2020-01-15",
          created_at: "2020-01-01T00:00:00",
          updated_at: "2020-01-01T00:00:00",
        },
      ],
      total: 1,
      page: 1,
      page_size: 25,
    });
    vi.spyOn(employeesApi, "fetchMetaFilters").mockResolvedValue({
      countries: ["US"],
      departments: ["Engineering"],
      job_titles: ["Engineer"],
    });

    render(wrap(<EmployeesPage />));

    expect(await screen.findByText("Jane Doe")).toBeInTheDocument();
    expect(screen.getByText("jane@acme.example")).toBeInTheDocument();
  });
});
