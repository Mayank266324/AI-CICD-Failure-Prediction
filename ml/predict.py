from pathlib import Path
import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIRECTORY = PROJECT_ROOT / "models"


class FailurePredictor:

    def __init__(self, model_name="xgboost"):

        model_path = (
            MODEL_DIRECTORY /
            f"{model_name}.pkl"
        )

        feature_path = (
            MODEL_DIRECTORY /
            "feature_names.pkl"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        if not feature_path.exists():
            raise FileNotFoundError(
                f"Feature file not found: {feature_path}"
            )

        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)

    def predict(self, data: dict):

        # Convert incoming data into DataFrame
        input_data = pd.DataFrame(
            [data]
        )

        # Ensure feature order is identical
        input_data = input_data[
            self.feature_names
        ]

        # Prediction
        prediction = self.model.predict(
            input_data
        )[0]

        # Failure probability
        probability = self.model.predict_proba(
            input_data
        )[0][1]

        risk_level = self._get_risk_level(
            probability
        )

        return {
            "prediction": (
                "failure"
                if prediction == 1
                else "success"
            ),
            "failure_probability": round(
                float(probability),
                4
            ),
            "failure_percentage": round(
                float(probability * 100),
                2
            ),
            "risk_level": risk_level
        }

    @staticmethod
    def _get_risk_level(probability):

        if probability <= 0.30:
            return "LOW"

        elif probability <= 0.60:
            return "MEDIUM"

        elif probability <= 0.80:
            return "HIGH"

        return "CRITICAL"