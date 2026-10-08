import json
import os
import subprocess
from pathlib import Path


def run_git_command(command):
    """
    Execute a git command and return stdout.
    """
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return ""

    return result.stdout.strip()


def get_changed_files():
    """
    Get number of files changed between the previous
    commit and the current commit.
    """

    output = run_git_command(
        "git diff --name-only HEAD^ HEAD"
    )

    if not output:
        return 0

    return len(
        [
            line
            for line in output.splitlines()
            if line.strip()
        ]
    )


def get_line_changes():
    """
    Get total lines added and deleted between
    the previous commit and current commit.
    """

    output = run_git_command(
        "git diff --numstat HEAD^ HEAD"
    )

    lines_added = 0
    lines_deleted = 0

    if not output:
        return lines_added, lines_deleted

    for line in output.splitlines():

        parts = line.split("\t")

        if len(parts) < 3:
            continue

        added = parts[0]
        deleted = parts[1]

        # Binary files may show "-"
        if added.isdigit():
            lines_added += int(added)

        if deleted.isdigit():
            lines_deleted += int(deleted)

    return lines_added, lines_deleted


def get_commit_frequency():
    """
    Approximate commit frequency as commits per day
    over the last 30 days.
    """

    output = run_git_command(
        'git log --since="30 days ago" --format=%H'
    )

    if not output:
        return 0.0

    commit_count = len(output.splitlines())

    return round(
        commit_count / 30.0,
        2
    )


def get_repository_info():

    repository = os.getenv(
        "GITHUB_REPOSITORY",
        "local/repository"
    )

    branch = os.getenv(
        "GITHUB_REF_NAME",
        "unknown"
    )

    commit_sha = os.getenv(
        "GITHUB_SHA",
        "unknown"
    )

    run_id = os.getenv(
        "GITHUB_RUN_ID",
        "local-run"
    )

    return {
        "repository": repository,
        "branch": branch,
        "commit_sha": commit_sha,
        "run_id": run_id,
    }


def collect_features():

    files_changed = get_changed_files()

    lines_added, lines_deleted = get_line_changes()

    commit_frequency = get_commit_frequency()

    repository_info = get_repository_info()

    features = {

        # ML features
        "files_changed": files_changed,

        "lines_added": lines_added,

        "lines_deleted": lines_deleted,

        "commit_frequency": commit_frequency,

        # These will be populated from historical
        # pipeline data in the next stage.
        "previous_failures": 0,

        "previous_runs": 0,

        "historical_failure_rate": 0.0,

        "test_count": 0,

        "test_failures": 0,

        "build_duration": 0,

        "dependency_changes": 0,

        # GitHub metadata
        "repository": repository_info["repository"],

        "branch": repository_info["branch"],

        "commit_sha": repository_info["commit_sha"],

        "run_id": repository_info["run_id"],
    }

    return features


def main():

    features = collect_features()

    output_path = Path(
        "data/github_actions_features.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            features,
            file,
            indent=4
        )

    print("\n===================================")
    print("GitHub Actions Feature Collector")
    print("===================================\n")

    for key, value in features.items():
        print(f"{key}: {value}")

    print(
        f"\nFeature file created: {output_path}"
    )


if __name__ == "__main__":
    main()