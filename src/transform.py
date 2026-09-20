"""
transform.py

Reads the cleaned raw trips table (built by the ingestion pipeline in the
companion "nyc-taxi-dimensional-warehouse" project), applies transformations
entirely inside Snowflake using Snowpark DataFrames, and writes the results
back as curated tables; no data ever leaves Snowflake's compute engine
during this process.
"""

from connection import get_session
from snowflake.snowpark.functions import col, when, round as sf_round

def run_transformations() -> None:
    session = get_session()
    print(f"Connected. Warehouse: {session.get_current_warehouse}")

    # Source: the cleaned table produced by the ingestion project
    trips = session.table("RAW.RAW_TRIPS_CLEAN")

    cleaned = (
        trips
        .filter((col("FARE_AMOUNT") > 0) & (col("TRIP_DISTANCE") > 0))
        .with_column(
            "TIP_PERCENTAGE",
            sf_round((col("TIP_AMOUNT") / col("FARE_AMOUNT")) * 100, 2),
        )
        .with_column(
            "TRIP_CATEGORY",
            when(col("TRIP_DISTANCE") < 2, "short")
            .when(col("TRIP_DISTANCE") < 10, "medium")
            .otherwise("long"),
        )
    )

    daily_summary = (
        cleaned
        .group_by(col("TRIP_CATEGORY"))
        .agg(
            {"TOTAL_AMOUNT": "sum", "TRIP_DISTANCE": "avg", "TIP_PERCENTAGE": "avg"}
        )
        .sort(col("TRIP_CATEGORY"))
    )

    print("\nPreview of transformed data:")
    cleaned.show(5)

    print("\nSummary by trip category:")
    daily_summary.show()

    cleaned.write.mode("overwrite").save_as_table("ANALYTICS.CURATED_TRIPS")
    daily_summary.write.mode("overwrite").save_as_table(
        "ANALYTICS.TRIP_CATEGORY_SUMMARY"
    )

    print("\nWrote ANALYTICS.CURATED_TRIPS and ANALYTICS.TRIP_CATEGORY_SUMMARY.")
    session.close()


if __name__ == "__main__":
    run_transformations()
