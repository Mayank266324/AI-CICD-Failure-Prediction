import json
from collections import defaultdict

from collections import Counter

from sqlalchemy.orm import Session

from .models import PipelinePrediction


def get_pipeline_analytics(db: Session):

    records = (
        db.query(PipelinePrediction)
        .order_by(PipelinePrediction.created_at.asc())
        .all()
    )

    total_pipelines = len(records)

    if total_pipelines == 0:
        return {
            "total_pipelines": 0,
            "predicted_failures": 0,
            "predicted_successes": 0,
            "failure_rate": 0.0,
            "average_failure_probability": 0.0,
            "risk_distribution": {
                "LOW": 0,
                "MEDIUM": 0,
                "HIGH": 0,
                "CRITICAL": 0
            }
        }

    predicted_failures = sum(
        1 for record in records
        if record.prediction == "failure"
    )

    predicted_successes = total_pipelines - predicted_failures

    failure_rate = (
        predicted_failures / total_pipelines
    ) * 100

    average_failure_probability = (
        sum(record.failure_probability for record in records)
        / total_pipelines
    ) * 100

    risk_counter = Counter(
        record.risk_level
        for record in records
    )

    risk_distribution = {
        "LOW": risk_counter.get("LOW", 0),
        "MEDIUM": risk_counter.get("MEDIUM", 0),
        "HIGH": risk_counter.get("HIGH", 0),
        "CRITICAL": risk_counter.get("CRITICAL", 0)
    }

    return {
        "total_pipelines": total_pipelines,
        "predicted_failures": predicted_failures,
        "predicted_successes": predicted_successes,
        "failure_rate": round(failure_rate, 2),
        "average_failure_probability": round(
            average_failure_probability,
            2
        ),
        "risk_distribution": risk_distribution
    }

def get_shap_analytics(db: Session):

    records = (
        db.query(PipelinePrediction)
        .order_by(PipelinePrediction.created_at.asc())
        .all()
    )

    feature_impacts = defaultdict(list)

    for record in records:

        if not record.explanation:
            continue

        try:
            explanations = json.loads(record.explanation)
        except json.JSONDecodeError:
            continue

        for item in explanations:

            feature = item.get("feature")
            impact = item.get("impact")

            if feature is None or impact is None:
                continue

            feature_impacts[feature].append(
                float(impact)
            )

    results = []

    for feature, impacts in feature_impacts.items():

        average_impact = sum(impacts) / len(impacts)

        average_absolute_impact = (
            sum(abs(value) for value in impacts)
            / len(impacts)
        )

        results.append({
            "feature": feature,
            "average_impact": round(
                average_impact,
                6
            ),
            "average_absolute_impact": round(
                average_absolute_impact,
                6
            ),
            "sample_count": len(impacts)
        })

    results.sort(
        key=lambda item: item["average_absolute_impact"],
        reverse=True
    )

    return results