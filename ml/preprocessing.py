import pandas as pd
from sklearn.model_selection import train_test_split


TARGET_COLUMN = "pipeline_status"


def load_dataset(path: str) -> pd.DataFrame:
    """
    Load CI/CD pipeline dataset from CSV.
    """

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


def prepare_features(df: pd.DataFrame):
    """
    Prepare input features and target variable.
    """

    df = df.copy()

    # Convert target:
    # success = 0
    # failure = 1
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map({
        "success": 0,
        "failure": 1
    })

    if df[TARGET_COLUMN].isna().any():
        raise ValueError(
            "Target column contains unknown values."
        )

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    return X, y


def split_dataset(X, y, test_size=0.2):
    """
    Split dataset into training and testing sets.
    """

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y
    )