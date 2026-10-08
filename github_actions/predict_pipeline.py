import json
import sys
from pathlib import Path

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "github_actions_features.json"


# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Import ML and database components
# ---------------------------------------------------------

from ml.predict import FailurePredictor
from ml.explain import FailureExplainer

from database.database import SessionLocal
from database.crud import create_prediction


# ---------------------------------------------------------
# Load collected features
# ---------------------------------------------------------

def load_features():

    if not DATA_FILE.exists():

        raise FileNotFoundError(
            f"Feature file not found: {DATA_FILE}"
        )

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        features = json.load(file)

    return features


# ---------------------------------------------------------
# Main prediction pipeline
# ---------------------------------------------------------

def run_prediction():

    print()
    print("===================================")
    print("AI CI/CD Pipeline Prediction")
    print("===================================")
    print()

    # -----------------------------------------------------
    # Load features
    # -----------------------------------------------------

    features = load_features()

    print("Loaded pipeline features:")
    print()

    for key, value in features.items():

        print(f"{key}: {value}")

    print()

    # -----------------------------------------------------
    # Initialize ML components
    # -----------------------------------------------------

    print("Loading XGBoost model...")

    predictor = FailurePredictor(
        model_name="xgboost"
    )

    print("Loading SHAP explainer...")

    explainer = FailureExplainer(
        model_name="xgboost"
    )

    print()

    # -----------------------------------------------------
    # Generate prediction
    # -----------------------------------------------------

    print("Generating pipeline prediction...")

    prediction_result = predictor.predict(
        features
    )

    # -----------------------------------------------------
    # Generate SHAP explanation
    # -----------------------------------------------------

    print("Generating SHAP explanation...")

    explanation = explainer.explain(
        features
    )

    prediction_result["explanation"] = explanation

    # -----------------------------------------------------
    # Display result
    # -----------------------------------------------------

    print()
    print("===================================")
    print("Prediction Result")
    print("===================================")
    print()

    print(
        f"Prediction          : "
        f"{prediction_result['prediction']}"
    )

    print(
        f"Failure Probability : "
        f"{prediction_result['failure_probability']:.4f}"
    )

    print(
        f"Failure Percentage  : "
        f"{prediction_result['failure_percentage']:.2f}%"
    )

    print(
        f"Risk Level          : "
        f"{prediction_result['risk_level']}"
    )

    print()

    print("SHAP Explanation:")
    print()

    for item in explanation:

        print(
            f"{item['feature']}: "
            f"{item['impact']:.6f} "
            f"({item['direction']})"
        )

    # -----------------------------------------------------
    # Save prediction to database
    # -----------------------------------------------------

    print()
    print("Saving prediction to database...")

    db = SessionLocal()

    try:

        create_prediction(
            db=db,
            features=features,
            prediction_result=prediction_result
        )

        print(
            "Prediction successfully saved "
            "to SQLite database."
        )

    finally:

        db.close()

    # -----------------------------------------------------
    # Save prediction result as JSON
    # -----------------------------------------------------

    output_file = (
        PROJECT_ROOT
        / "data"
        / "github_actions_prediction.json"
    )

    output_data = {
        "features": features,
        "prediction": prediction_result
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output_data,
            file,
            indent=4
        )

    print(
        f"Prediction result saved to: "
        f"{output_file}"
    )

    print()
    print("===================================")
    print("Pipeline Prediction Complete")
    print("===================================")
    print()

    return prediction_result


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":

    try:

        run_prediction()

    except Exception as error:

        print()
        print("===================================")
        print("Prediction Failed")
        print("===================================")
        print()

        print(f"Error: {error}")

        print()

        raise