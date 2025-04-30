from pathlib import Path
import sqlite3
from config import PROJECT_ROOT
import db
from repositories.general_statistics_repository import GeneralStatisticsRepository
from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.general_statistics_service import GeneralStatisticsService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService


def create_test_database_connection():
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    schema_path = Path(PROJECT_ROOT) / "data" / "schema.sql"
    with schema_path.open() as f:
        connection.executescript(f.read())

    seed_data_path = Path(PROJECT_ROOT) / "data" / "seed_data.sql"
    with seed_data_path.open() as f:
        connection.executescript(f.read())

    return connection


def get_database(db_connection):
    return db.Database(connection=db_connection)


def get_user_service(db):
    user_repository = UserRepository(db)
    return UserService(user_repository)


def get_general_statistics_service(db):
    general_stats_repository = GeneralStatisticsRepository(db)
    return GeneralStatisticsService(
        general_stats_repository)


def get_user_statistics_service(db):
    user_statistics_repository = UserStatisticsRepository(db)
    return UserStatisticsService(
        user_statistics_repository)
