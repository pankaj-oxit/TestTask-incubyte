export type InsightsSummary = {
  headcount: number;
  average_salary_usd: number;
  median_salary_usd: number;
};

export type CountryInsight = {
  country_code: string;
  headcount: number;
  min_salary_local: number;
  max_salary_local: number;
  average_salary_local: number;
  median_salary_local: number;
  min_salary_usd: number;
  max_salary_usd: number;
  average_salary_usd: number;
  median_salary_usd: number;
};

export type JobTitleInsight = {
  job_title: string;
  headcount: number;
  min_salary_usd: number;
  max_salary_usd: number;
  average_salary_usd: number;
  median_salary_usd: number;
};

export type DistributionBucket = {
  range: string;
  count: number;
};

export type DistributionInsight = {
  headcount: number;
  buckets: DistributionBucket[];
};
