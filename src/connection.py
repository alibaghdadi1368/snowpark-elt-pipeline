"""
connection.py

Creates and returns a Snowpark Session using credentials loaded from a
local .env file. This file is never committed with real credentials.
See conf/.env.example for the expected format.
"""

import os
from dotenv import load_dotenv
from snowflake.snowpark import Session


load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", ".env"))


def get_session() -> Session:
    """
    Build a Snowpark Session from environment variables.

    Raises:
        ValueError: if any required connection parameter is missing.
    """
    required_vars = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_ROLE",
    ]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Copy config/.env.example to config/.env and add fill in your own values."
        )


    connection_params = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        "role": os.getenv("SNOWFLAKE_ROLE")
    }
    return Session.builder.configs(connection_params).create()

if __name__ == "__main__":
    # Quick manual connectivity check: python connection.py
    session = get_session()
    print("Connection successfully.")
    print("Warehouse:", session.get_current_warehouse())
    print("Database:", session.get_current_database())
    print("Schema:", session.get_current_schema())
    session.close()