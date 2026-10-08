from pathlib import Path

import joblib
import pandas as pd
import shap


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIRECTORY = PROJECT_ROOT / "models"


class FailureExplainer:

    def __init__(self, model_name="xgboost"):
        model_path = MODEL_DIRECTORY / f"{model_name}.pkl"
        feature_path = MODEL_DIRECTORY / "feature_names.pkl"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        if not feature_path.exists():
            raise FileNotFoundError(
                f"Feature names not found: {feature_path}"
            )

        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)

        self.explainer = shap.TreeExplainer(self.model)

    def explain(self, data: dict):

        input_data = pd.DataFrame([data])

        input_data = input_data[self.feature_names]

        shap_values = self.explainer.shap_values(input_data)

        # XGBoost binary classification
        if isinstance(shap_values, list):
            values = shap_values[1][0]
        else:
            values = shap_values[0]

        explanation = []

        for feature, value in zip(self.feature_names, values):
            explanation.append({
                "feature": feature,
                "impact": round(float(value), 6),
                "direction": (
                    "increases_failure_risk"
                    if value > 0
                    else "decreases_failure_risk"
                )
            })

        explanation.sort(
            key=lambda x: abs(x["impact"]),
            reverse=True
        )

        return explanation