from pydantic import BaseModel


class InsightsSummaryResponse(BaseModel):
    headcount: int
    average_salary_usd: float
    median_salary_usd: float


class CountryInsightRow(BaseModel):
    country_code: str
    headcount: int
    min_salary_local: int
    max_salary_local: int
    average_salary_local: float
    median_salary_local: float
    min_salary_usd: float
    max_salary_usd: float
    average_salary_usd: float
    median_salary_usd: float


class JobTitleInsightRow(BaseModel):
    job_title: str
    headcount: int
    min_salary_usd: float
    max_salary_usd: float
    average_salary_usd: float
    median_salary_usd: float


class DistributionBucket(BaseModel):
    range: str
    count: int


class DistributionResponse(BaseModel):
    headcount: int
    buckets: list[DistributionBucket]
