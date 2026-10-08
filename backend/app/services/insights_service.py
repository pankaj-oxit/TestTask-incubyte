from collections import defaultdict

from app.core.stats import distribution_buckets_usd, median
from app.repositories.insights_repository import InsightsRepository
from app.schemas.insights import (
    CountryInsightRow,
    DistributionResponse,
    InsightsSummaryResponse,
    JobTitleInsightRow,
)
from app.services.currency_service import to_usd


class InsightsService:
    def __init__(self, repo: InsightsRepository):
        self._repo = repo

    def summary(self) -> InsightsSummaryResponse:
        rows = self._repo.list_salary_rows()
        usd_amounts = [to_usd(salary, currency) for _, _, currency, salary in rows]
        if not usd_amounts:
            return InsightsSummaryResponse(headcount=0, average_salary_usd=0.0, median_salary_usd=0.0)
        return InsightsSummaryResponse(
            headcount=len(usd_amounts),
            average_salary_usd=round(sum(usd_amounts) / len(usd_amounts), 2),
            median_salary_usd=round(median(usd_amounts), 2),
        )

    def by_country(self, *, country_code: str | None = None) -> list[CountryInsightRow]:
        rows = self._repo.list_salary_rows(country_code=country_code)
        grouped: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for country, _, currency, salary in rows:
            grouped[country].append((currency, salary))

        result: list[CountryInsightRow] = []
        for code in sorted(grouped):
            country_code = code
            entries = grouped[code]
            local_salaries = [salary for _, salary in entries]
            usd_amounts = [to_usd(salary, currency) for currency, salary in entries]
            result.append(
                CountryInsightRow(
                    country_code=country_code,
                    headcount=len(entries),
                    min_salary_local=min(local_salaries),
                    max_salary_local=max(local_salaries),
                    average_salary_local=round(sum(local_salaries) / len(local_salaries), 2),
                    median_salary_local=round(median([float(s) for s in local_salaries]), 2),
                    min_salary_usd=min(usd_amounts),
                    max_salary_usd=max(usd_amounts),
                    average_salary_usd=round(sum(usd_amounts) / len(usd_amounts), 2),
                    median_salary_usd=round(median(usd_amounts), 2),
                )
            )
        return result

    def by_job_title(
        self,
        *,
        job_title: str | None = None,
        country_code: str | None = None,
    ) -> list[JobTitleInsightRow]:
        rows = self._repo.list_salary_rows(country_code=country_code, job_title=job_title)
        grouped: dict[str, list[float]] = defaultdict(list)
        for _, row_job_title, currency, salary in rows:
            grouped[row_job_title].append(to_usd(salary, currency))

        result: list[JobTitleInsightRow] = []
        for title in sorted(grouped):
            usd_amounts = grouped[title]
            result.append(
                JobTitleInsightRow(
                    job_title=title,
                    headcount=len(usd_amounts),
                    min_salary_usd=min(usd_amounts),
                    max_salary_usd=max(usd_amounts),
                    average_salary_usd=round(sum(usd_amounts) / len(usd_amounts), 2),
                    median_salary_usd=round(median(usd_amounts), 2),
                )
            )
        return result

    def distribution(
        self,
        *,
        country_code: str | None = None,
        job_title: str | None = None,
    ) -> DistributionResponse:
        rows = self._repo.list_salary_rows(country_code=country_code, job_title=job_title)
        usd_amounts = [to_usd(salary, currency) for _, _, currency, salary in rows]
        buckets = distribution_buckets_usd(usd_amounts)
        return DistributionResponse(headcount=len(usd_amounts), buckets=buckets)
