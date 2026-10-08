from explain import FailureExplainer


def main():

    explainer = FailureExplainer(model_name="xgboost")

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

    results = explainer.explain(sample_pipeline)

    print("\nSHAP Explanation")
    print("=" * 60)

    for item in results:
        print(
            f"{item['feature']:25} "
            f"{item['impact']:>10}   "
            f"{item['direction']}"
        )


if __name__ == "__main__":
    main()