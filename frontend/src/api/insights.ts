import { apiFetch } from "./client";
import type {
  CountryInsight,
  DistributionInsight,
  InsightsSummary,
  JobTitleInsight,
} from "../types/insights";

export function fetchInsightsSummary(): Promise<InsightsSummary> {
  return apiFetch<InsightsSummary>("/insights/summary");
}

export function fetchInsightsByCountry(country?: string): Promise<CountryInsight[]> {
  const q = country ? `?country=${encodeURIComponent(country)}` : "";
  return apiFetch<CountryInsight[]>(`/insights/by-country${q}`);
}

export function fetchInsightsByJobTitle(params?: {
  job_title?: string;
  country?: string;
}): Promise<JobTitleInsight[]> {
  const q = new URLSearchParams();
  if (params?.job_title) q.set("job_title", params.job_title);
  if (params?.country) q.set("country", params.country);
  const qs = q.toString();
  return apiFetch<JobTitleInsight[]>(`/insights/by-job-title${qs ? `?${qs}` : ""}`);
}

export function fetchInsightsDistribution(params?: {
  country?: string;
  job_title?: string;
}): Promise<DistributionInsight> {
  const q = new URLSearchParams();
  if (params?.country) q.set("country", params.country);
  if (params?.job_title) q.set("job_title", params.job_title);
  const qs = q.toString();
  return apiFetch<DistributionInsight>(`/insights/distribution${qs ? `?${qs}` : ""}`);
}
