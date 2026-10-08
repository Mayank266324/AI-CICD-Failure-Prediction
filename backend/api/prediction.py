from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.crud import create_prediction
from database.database import get_db

from ..schemas.prediction_schema import (
    PipelineFeatures,
    PredictionResponse
)

from ..services.prediction_service import PredictionService


router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"]
)


prediction_service = PredictionService()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict_pipeline(
    features: PipelineFeatures,
    db: Session = Depends(get_db)
):

    feature_data = features.model_dump()

    # Generate prediction + SHAP explanation
    result = prediction_service.predict(feature_data)

    # Save prediction to database
    create_prediction(
        db=db,
        features=feature_data,
        prediction_result=result
    )

    return result