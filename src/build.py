import subprocess
from pathlib import Path


def build_database():
    db_path = Path("data/database.db")
    schema_path = Path("data/schema.sql")

    if db_path.exists():
        print("Database already exists.")
        return

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
    except subprocess.CalledProcessError as e:
        print("Failed to create database.")
        print(e)


if __name__ == "__main__":
    build_database()
