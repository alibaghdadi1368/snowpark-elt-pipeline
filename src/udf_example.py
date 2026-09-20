"""
udf_example.py

Registers a Python UDF inside Snowflake that classifies trip quality
based on tip percentage, then demonstrates using it in a SQL query.
Requires transform.py to have been run first (ANALYTICS.CURATED_TRIPS
must exist).
"""

from connection import get_session
from snowflake.snowpark.types import StringType, FloatType

def classify_trip_quality(tip_percentage: float) -> str:
    """Classify a trip's tip percentage into a quality bucket."""
    if tip_percentage is None:
        return "unknown"
    if tip_percentage >= 20:
        return "excellent"
    if tip_percentage >= 10:
        return "good"
    else:
        return "low"

def register_udf() -> None:
    session = get_session()

    session.udf.register(
        func=classify_trip_quality,
        return_type=StringType(),
        input_type=[FloatType()],
        name="Classify_trip_quality_udf",
        is_permanent=True,
        stage_location="@raw.s3_raw_stage",
        replace=True
    )
    print("Registered classify_trip_quality_udf.")

    print("\nSample output:")
    session.sql(
        """
        SELECT
            TIP_PERCENTAGE,
            classify_trip_quality_udf(TIP_PERCENTAGE) as quality
        FROM ANALYTICS.CURATED_TRIPS
        LIMIT 10
        """
    ).show()

    session.close()

if __name__ == "__main__":
    register_udf()