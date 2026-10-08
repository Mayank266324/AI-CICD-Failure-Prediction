import os
import joblib
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from preprocessing import (
    load_dataset,
    prepare_features,
    split_dataset
)


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "pipeline_data.csv"
MODEL_DIRECTORY = PROJECT_ROOT / "models"


def train_models():

    print("Loading dataset...")

    df = load_dataset(DATASET_PATH)

    print(f"Dataset shape: {df.shape}")

    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    models = {

        "logistic_regression": LogisticRegression(
            max_iter=1000
        ),

        "random_forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        ),

        "xgboost": XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.05,
            random_state=42,
            eval_metric="logloss"
        )
    }

    os.makedirs(MODEL_DIRECTORY, exist_ok=True)

    for model_name, model in models.items():

        print(
            f"\nTraining {model_name}..."
        )

        model.fit(
            X_train,
            y_train
        )

        model_path = os.path.join(
            MODEL_DIRECTORY,
            f"{model_name}.pkl"
        )

        joblib.dump(
            model,
            model_path
        )

        print(
            f"Saved model → {model_path}"
        )

    # Save feature names for later prediction
    feature_path = os.path.join(
        MODEL_DIRECTORY,
        "feature_names.pkl"
    )

    joblib.dump(
        list(X.columns),
        feature_path
    )

    print("\nTraining completed successfully.")


if __name__ == "__main__":
    train_models()