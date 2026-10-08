import sqlite3
from pathlib import Path


# -------------------------------------------------
# Project paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "database"
    / "cicd_predictions.db"
)


def migrate_database():

    print()
    print("===================================")
    print("Database Migration")
    print("===================================")
    print()

    print(f"Database: {DATABASE_PATH}")
    print()

    if not DATABASE_PATH.exists():

        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    # -------------------------------------------------
    # Get existing columns
    # -------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(pipeline_predictions)"
    )

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    # -------------------------------------------------
    # GitHub metadata columns
    # -------------------------------------------------

    new_columns = {

        "repository":
            "VARCHAR(255)",

        "branch":
            "VARCHAR(255)",

        "commit_sha":
            "VARCHAR(255)",

        "run_id":
            "VARCHAR(255)"
    }

    # -------------------------------------------------
    # Add missing columns
    # -------------------------------------------------

    for column_name, column_type in new_columns.items():

        if column_name in existing_columns:

            print(
                f"[EXISTS] {column_name}"
            )

            continue

        sql = (
            f"ALTER TABLE pipeline_predictions "
            f"ADD COLUMN {column_name} {column_type}"
        )

        cursor.execute(sql)

        print(
            f"[ADDED]  {column_name}"
        )

    connection.commit()

    # -------------------------------------------------
    # Verify migration
    # -------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(pipeline_predictions)"
    )

    columns = cursor.fetchall()

    print()
    print("Current database columns:")
    print()

    for column in columns:

        print(
            f"- {column[1]}"
        )

    connection.close()

    print()
    print(
        "Database migration completed successfully."
    )
    print()


if __name__ == "__main__":

    migrate_database()