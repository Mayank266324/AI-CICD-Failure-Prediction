from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.analytics import (
    get_pipeline_analytics,
    get_shap_analytics
)

from database.database import get_db

from ..schemas.prediction_schema import (
    AnalyticsResponse,
    SHAPAnalyticsResponse
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Analytics"]
)


@router.get(
    "/analytics",
    response_model=AnalyticsResponse
)
def pipeline_analytics(
    db: Session = Depends(get_db)
):

    return get_pipeline_analytics(db)


@router.get(
    "/analytics/shap",
    response_model=SHAPAnalyticsResponse
)
def shap_analytics(
    db: Session = Depends(get_db)
):

    results = get_shap_analytics(db)

    return {
        "total_features": len(results),
        "features": results
    }