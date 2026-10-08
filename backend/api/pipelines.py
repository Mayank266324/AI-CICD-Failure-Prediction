import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.crud import (
    get_predictions,
    get_prediction_by_id
)

from ..schemas.prediction_schema import (
    PipelineHistoryResponse
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Pipeline History"]
)


def convert_prediction(record):

    explanation = []

    if record.explanation:

        try:
            explanation = json.loads(
                record.explanation
            )

        except json.JSONDecodeError:

            explanation = []

    return {

        # -------------------------------------------------
        # Basic record information
        # -------------------------------------------------

        "id": record.id,

        # -------------------------------------------------
        # GitHub / CI metadata
        # -------------------------------------------------

        "repository": record.repository,

        "branch": record.branch,

        "commit_sha": record.commit_sha,

        "run_id": record.run_id,

        # -------------------------------------------------
        # Pipeline input features
        # -------------------------------------------------

        "files_changed": record.files_changed,

        "lines_added": record.lines_added,

        "lines_deleted": record.lines_deleted,

        "previous_failures": record.previous_failures,

        "previous_runs": record.previous_runs,

        "historical_failure_rate": (
            record.historical_failure_rate
        ),

        "test_count": record.test_count,

        "test_failures": record.test_failures,

        "build_duration": record.build_duration,

        "dependency_changes": (
            record.dependency_changes
        ),

        "commit_frequency": (
            record.commit_frequency
        ),

        # -------------------------------------------------
        # ML prediction
        # -------------------------------------------------

        "prediction": record.prediction,

        "failure_probability": (
            record.failure_probability
        ),

        "failure_percentage": (
            record.failure_percentage
        ),

        "risk_level": record.risk_level,

        # -------------------------------------------------
        # SHAP explanation
        # -------------------------------------------------

        "explanation": explanation,

        # -------------------------------------------------
        # Timestamp
        # -------------------------------------------------

        "created_at": record.created_at
    }


@router.get(
    "/pipelines",
    response_model=list[PipelineHistoryResponse]
)
def list_pipelines(
    limit: int = 50,
    db: Session = Depends(get_db)
):

    records = get_predictions(
        db=db,
        limit=limit
    )

    return [
        convert_prediction(record)
        for record in records
    ]


@router.get(
    "/pipelines/{prediction_id}",
    response_model=PipelineHistoryResponse
)
def get_pipeline(
    prediction_id: int,
    db: Session = Depends(get_db)
):

    record = get_prediction_by_id(
        db=db,
        prediction_id=prediction_id
    )

    if record is None:

        raise HTTPException(
            status_code=404,
            detail="Prediction not found."
        )

    return convert_prediction(record)