import subprocess
from pathlib import Path


def build_database(database_name="database"):
    """
    This script creates a new SQLite database from a schema.sql file if the database does not already exist.

    Functions:
        - build_database(database_name="database"):
            Creates a SQLite database under the 'data/' folder using a predefined schema.
            If the database already exists, the creation is skipped. This prevents accidental db deletion. 
            Executes the SQL schema file via subprocess.

    Usage:
        Run the script directly to create the database:
            python build_database.py
    """

    db_path = Path(f"data/{database_name}.db")
    schema_path = Path("data/schema.sql")

    if db_path.exists():
        print("Database already exists.")
        return False

    print("Creating database using schema.sql...")

    # equivalent of: sqlite3 database.db < data/schema.sql
    try:
        subprocess.run(
            ["sqlite3", str(db_path)],
            input=schema_path.read_text(encoding="utf-8"),
            text=True,
            check=True
        )
        print("Database created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to create database.")
        print(e)
        return False


if __name__ == "__main__":
    build_database()
