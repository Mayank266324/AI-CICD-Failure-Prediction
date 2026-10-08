import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ML_DIRECTORY = PROJECT_ROOT / "ml"

if str(ML_DIRECTORY) not in sys.path:
    sys.path.append(str(ML_DIRECTORY))

from predict import FailurePredictor
from explain import FailureExplainer


class PredictionService:

    def __init__(self):
        self.predictor = FailurePredictor(model_name="xgboost")
        self.explainer = FailureExplainer(model_name="xgboost")

    def predict(self, features: dict):

        prediction_result = self.predictor.predict(features)

        explanation = self.explainer.explain(features)

        prediction_result["explanation"] = explanation

        return prediction_result