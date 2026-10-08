import json

from sqlalchemy.orm import Session

from .models import PipelinePrediction


def create_prediction(
    db: Session,
    features: dict,
    prediction_result: dict
):

    explanation = prediction_result.get(
        "explanation",
        []
    )

    db_prediction = PipelinePrediction(

        # -------------------------------------------------
        # GitHub / CI metadata
        # -------------------------------------------------

        repository=features.get(
            "repository"
        ),

        branch=features.get(
            "branch"
        ),

        commit_sha=features.get(
            "commit_sha"
        ),

        run_id=features.get(
            "run_id"
        ),

        # -------------------------------------------------
        # Pipeline input features
        # -------------------------------------------------

        files_changed=features["files_changed"],

        lines_added=features["lines_added"],

        lines_deleted=features["lines_deleted"],

        previous_failures=features["previous_failures"],

        previous_runs=features["previous_runs"],

        historical_failure_rate=(
            features["historical_failure_rate"]
        ),

        test_count=features["test_count"],

        test_failures=features["test_failures"],

        build_duration=features["build_duration"],

        dependency_changes=features["dependency_changes"],

        commit_frequency=features["commit_frequency"],

        # -------------------------------------------------
        # ML prediction
        # -------------------------------------------------

        prediction=prediction_result["prediction"],

        failure_probability=(
            prediction_result["failure_probability"]
        ),

        failure_percentage=(
            prediction_result["failure_percentage"]
        ),

        risk_level=prediction_result["risk_level"],

        # -------------------------------------------------
        # SHAP explanation
        # -------------------------------------------------

        explanation=json.dumps(
            explanation
        )
    )

    db.add(db_prediction)

    db.commit()

    db.refresh(db_prediction)

    return db_prediction


def get_predictions(
    db: Session,
    limit: int = 50
):

    return (
        db.query(PipelinePrediction)
        .order_by(
            PipelinePrediction.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def get_prediction(
    db: Session,
    prediction_id: int
):

    return (
        db.query(PipelinePrediction)
        .filter(
            PipelinePrediction.id == prediction_id
        )
        .first()
    )


def get_prediction_by_id(
    db: Session,
    prediction_id: int
):

    return (
        db.query(PipelinePrediction)
        .filter(
            PipelinePrediction.id == prediction_id
        )
        .first()
    )