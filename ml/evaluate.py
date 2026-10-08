import os
import joblib
import pandas as pd
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from preprocessing import (
    load_dataset,
    prepare_features,
    split_dataset
)


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "pipeline_data.csv"
MODEL_DIRECTORY = PROJECT_ROOT / "models"


def evaluate_model(model_name, X_test, y_test):

    model_path = os.path.join(
        MODEL_DIRECTORY,
        f"{model_name}.pkl"
    )

    model = joblib.load(model_path)

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    print("\n" + "=" * 60)
    print(f"MODEL: {model_name.upper()}")
    print("=" * 60)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Success",
                "Failure"
            ],
            zero_division=0
        )
    )

    return {
        "model": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc
    }


def main():

    df = load_dataset(DATASET_PATH)

    X, y = prepare_features(df)

    _, X_test, _, y_test = split_dataset(
        X,
        y
    )

    model_names = [
        "logistic_regression",
        "random_forest",
        "xgboost"
    ]

    results = []

    for model_name in model_names:

        result = evaluate_model(
            model_name,
            X_test,
            y_test
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    print("\n\nMODEL COMPARISON")
    print("=" * 60)

    print(
        results_df.sort_values(
            "f1",
            ascending=False
        ).to_string(index=False)
    )


if __name__ == "__main__":
    main()