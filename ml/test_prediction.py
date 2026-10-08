from predict import FailurePredictor


def main():

    predictor = FailurePredictor(
        model_name="xgboost"
    )

    sample_pipeline = {

        "files_changed": 35,

        "lines_added": 1200,

        "lines_deleted": 200,

        "previous_failures": 5,

        "previous_runs": 20,

        "historical_failure_rate": 0.25,

        "test_count": 150,

        "test_failures": 3,

        "build_duration": 480,

        "dependency_changes": 2,

        "commit_frequency": 5.2
    }

    result = predictor.predict(
        sample_pipeline
    )

    print("\nPrediction Result")
    print("=" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()