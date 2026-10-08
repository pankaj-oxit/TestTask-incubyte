from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.insights_repository import InsightsRepository
from app.schemas.insights import (
    CountryInsightRow,
    DistributionResponse,
    InsightsSummaryResponse,
    JobTitleInsightRow,
)
from app.services.insights_service import InsightsService

router = APIRouter(prefix="/insights", tags=["insights"])


def get_insights_service(db: Session = Depends(get_db)) -> InsightsService:
    return InsightsService(InsightsRepository(db))


@router.get("/summary", response_model=InsightsSummaryResponse)
def insights_summary(service: InsightsService = Depends(get_insights_service)) -> InsightsSummaryResponse:
    return service.summary()


@router.get("/by-country", response_model=list[CountryInsightRow])
def insights_by_country(
    country: str | None = Query(
        None,
        min_length=2,
        max_length=2,
        description="Optional ISO country code; omit to list all countries",
    ),
    service: InsightsService = Depends(get_insights_service),
) -> list[CountryInsightRow]:
    return service.by_country(country_code=country)


@router.get("/by-job-title", response_model=list[JobTitleInsightRow])
def insights_by_job_title(
    job_title: str | None = Query(
        None,
        min_length=1,
        max_length=100,
        description="Optional job title; omit to list all job titles",
    ),
    country: str | None = Query(
        None,
        min_length=2,
        max_length=2,
        description="Optional scope: only employees in this country",
    ),
    service: InsightsService = Depends(get_insights_service),
) -> list[JobTitleInsightRow]:
    return service.by_job_title(job_title=job_title, country_code=country)


@router.get("/distribution", response_model=DistributionResponse)
def insights_distribution(
    country: str | None = Query(None, min_length=2, max_length=2),
    job_title: str | None = Query(None, min_length=1, max_length=100),
    service: InsightsService = Depends(get_insights_service),
) -> DistributionResponse:
    return service.distribution(country_code=country, job_title=job_title)
