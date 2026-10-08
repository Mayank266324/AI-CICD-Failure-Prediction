from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from .database import Base


class PipelinePrediction(Base):

    __tablename__ = "pipeline_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -------------------------------------------------
    # GitHub / CI metadata
    # -------------------------------------------------

    repository = Column(
        String(255),
        nullable=True
    )

    branch = Column(
        String(255),
        nullable=True
    )

    commit_sha = Column(
        String(255),
        nullable=True
    )

    run_id = Column(
        String(255),
        nullable=True
    )

    # -------------------------------------------------
    # Pipeline input features
    # -------------------------------------------------

    files_changed = Column(
        Integer,
        nullable=False
    )

    lines_added = Column(
        Integer,
        nullable=False
    )

    lines_deleted = Column(
        Integer,
        nullable=False
    )

    previous_failures = Column(
        Integer,
        nullable=False
    )

    previous_runs = Column(
        Integer,
        nullable=False
    )

    historical_failure_rate = Column(
        Float,
        nullable=False
    )

    test_count = Column(
        Integer,
        nullable=False
    )

    test_failures = Column(
        Integer,
        nullable=False
    )

    build_duration = Column(
        Float,
        nullable=False
    )

    dependency_changes = Column(
        Integer,
        nullable=False
    )

    commit_frequency = Column(
        Float,
        nullable=False
    )

    # -------------------------------------------------
    # ML prediction
    # -------------------------------------------------

    prediction = Column(
        String(20),
        nullable=False
    )

    failure_probability = Column(
        Float,
        nullable=False
    )

    failure_percentage = Column(
        Float,
        nullable=False
    )

    risk_level = Column(
        String(20),
        nullable=False
    )

    # -------------------------------------------------
    # SHAP explanation
    # -------------------------------------------------

    explanation = Column(
        Text,
        nullable=True
    )

    # -------------------------------------------------
    # Timestamp
    # -------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )