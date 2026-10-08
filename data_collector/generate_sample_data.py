import os
import numpy as np
import pandas as pd


RANDOM_SEED = 42
NUM_SAMPLES = 5000

np.random.seed(RANDOM_SEED)


def generate_dataset():
    """
    Generate a synthetic CI/CD pipeline dataset.

    This dataset is ONLY for developing and testing the ML pipeline.
    It will later be replaced/augmented with real CI/CD data.
    """

    files_changed = np.random.poisson(lam=8, size=NUM_SAMPLES)
    files_changed = np.clip(files_changed, 1, 100)

    lines_added = np.random.gamma(
        shape=2.0,
        scale=50,
        size=NUM_SAMPLES
    ).astype(int)

    lines_deleted = np.random.gamma(
        shape=1.5,
        scale=30,
        size=NUM_SAMPLES
    ).astype(int)

    previous_failures = np.random.poisson(
        lam=1.5,
        size=NUM_SAMPLES
    )

    previous_runs = np.random.randint(
        5,
        50,
        size=NUM_SAMPLES
    )

    test_count = np.random.randint(
        20,
        300,
        size=NUM_SAMPLES
    )

    test_failures = np.random.binomial(
        test_count,
        0.03
    )

    build_duration = np.random.gamma(
        shape=4,
        scale=60,
        size=NUM_SAMPLES
    )

    dependency_changes = np.random.binomial(
        3,
        0.2,
        size=NUM_SAMPLES
    )

    commit_frequency = np.random.uniform(
        0.1,
        10,
        size=NUM_SAMPLES
    )

    # Historical failure rate
    previous_successes = previous_runs - previous_failures

    historical_failure_rate = (
        previous_failures / previous_runs
    )

    # Create a probability-like score.
    # This intentionally introduces relationships between
    # pipeline characteristics and failures.
    risk_score = (
        0.025 * files_changed
        + 0.0008 * lines_added
        + 0.001 * lines_deleted
        + 0.20 * previous_failures
        + 1.5 * historical_failure_rate
        + 0.15 * test_failures
        + 0.15 * dependency_changes
        + 0.0008 * build_duration
        + 0.03 * commit_frequency
        - 2.5
    )

    probability = 1 / (1 + np.exp(-risk_score))

    pipeline_status = np.random.binomial(
        1,
        probability
    )

    df = pd.DataFrame({
        "files_changed": files_changed,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "previous_failures": previous_failures,
        "previous_runs": previous_runs,
        "historical_failure_rate": historical_failure_rate,
        "test_count": test_count,
        "test_failures": test_failures,
        "build_duration": build_duration,
        "dependency_changes": dependency_changes,
        "commit_frequency": commit_frequency,
        "pipeline_status": pipeline_status
    })

    # Convert numerical target into human-readable labels
    df["pipeline_status"] = df["pipeline_status"].map({
        0: "success",
        1: "failure"
    })

    return df


def main():
    output_directory = "data/raw"
    output_file = os.path.join(
        output_directory,
        "pipeline_data.csv"
    )

    os.makedirs(output_directory, exist_ok=True)

    df = generate_dataset()

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Dataset generated successfully.")
    print(f"Location: {output_file}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\nClass distribution:")
    print(df["pipeline_status"].value_counts())
    print("\nFirst five records:")
    print(df.head())


if __name__ == "__main__":
    main()