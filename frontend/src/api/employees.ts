import { apiFetch } from "./client";
import type { Employee, EmployeeInput, EmployeeListResponse, ListEmployeesParams, MetaFilters } from "../types/employee";

function toQuery(params: ListEmployeesParams): string {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {
      q.set(key, String(value));
    }
  });
  const s = q.toString();
  return s ? `?${s}` : "";
}

export function listEmployees(params: ListEmployeesParams = {}): Promise<EmployeeListResponse> {
  return apiFetch<EmployeeListResponse>(`/employees${toQuery(params)}`);
}

export function getEmployee(id: number): Promise<Employee> {
  return apiFetch<Employee>(`/employees/${id}`);
}

export function createEmployee(payload: EmployeeInput): Promise<Employee> {
  return apiFetch<Employee>("/employees", { method: "POST", body: JSON.stringify(payload) });
}

export function updateEmployee(id: number, payload: EmployeeInput): Promise<Employee> {
  return apiFetch<Employee>(`/employees/${id}`, { method: "PUT", body: JSON.stringify(payload) });
}

export function deleteEmployee(id: number): Promise<void> {
  return apiFetch<void>(`/employees/${id}`, { method: "DELETE" });
}

export function fetchMetaFilters(): Promise<MetaFilters> {
  return apiFetch<MetaFilters>("/meta/filters");
}

export type HealthResponse = { status: string; employee_count: number };

export function fetchHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/health");
}
