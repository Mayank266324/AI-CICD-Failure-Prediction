from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class PipelineFeatures(BaseModel):

    files_changed: int = Field(ge=0)
    lines_added: int = Field(ge=0)
    lines_deleted: int = Field(ge=0)

    previous_failures: int = Field(ge=0)
    previous_runs: int = Field(ge=1)

    historical_failure_rate: float = Field(
        ge=0,
        le=1
    )

    test_count: int = Field(ge=0)
    test_failures: int = Field(ge=0)

    build_duration: float = Field(ge=0)

    dependency_changes: int = Field(ge=0)
    commit_frequency: float = Field(ge=0)


class FeatureExplanation(BaseModel):

    feature: str
    impact: float
    direction: str


class PredictionResponse(BaseModel):

    prediction: str
    failure_probability: float
    failure_percentage: float
    risk_level: str

    explanation: List[FeatureExplanation]


# -----------------------------------------
# Database response schemas
# -----------------------------------------

class PipelineHistoryResponse(BaseModel):

    id: int

    files_changed: int
    lines_added: int
    lines_deleted: int

    previous_failures: int
    previous_runs: int

    historical_failure_rate: float

    test_count: int
    test_failures: int

    build_duration: float

    dependency_changes: int
    commit_frequency: float

    prediction: str

    failure_probability: float
    failure_percentage: float

    risk_level: str

    explanation: List[FeatureExplanation]

    created_at: datetime

    class Config:
        from_attributes = True

class RiskDistribution(BaseModel):

    LOW: int
    MEDIUM: int
    HIGH: int
    CRITICAL: int


class AnalyticsResponse(BaseModel):

    total_pipelines: int

    predicted_failures: int
    predicted_successes: int

    failure_rate: float

    average_failure_probability: float

    risk_distribution: RiskDistribution

class SHAPFeatureAnalytics(BaseModel):

    feature: str
    average_impact: float
    average_absolute_impact: float
    sample_count: int


class SHAPAnalyticsResponse(BaseModel):

    total_features: int
    features: List[SHAPFeatureAnalytics]