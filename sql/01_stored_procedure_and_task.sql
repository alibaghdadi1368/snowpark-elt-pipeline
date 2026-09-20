-- ============================================================
-- Stored Procedure + Task: orchestration demonstration
-- The task is intentionally left SUSPENDED. It demonstrates the
-- pattern without consuming unnecessary credits.
-- ============================================================

use WAREHOUSE DEV_WH;
use DATABASE portfolio_db;
use SCHEMA portfolio_db.analytics;

create or replace PROCEDURE refresh_curated_trips()
RETURNS STRING
language PYTHON
runtime_version = '3.10'
packages = ('snowflake-snowpark-python')
handler = 'main'
as 
$$
def main(session):
    trips = session.table("RAW.RAW_TRIPS_CLEAN")
    cleaned = trips.filter(trips["FARE_AMOUNT"] > 0)
    cleaned.write.mode("overwrite").save_as_table("ANALYTICS.CURATED_TRIPS")
    return "Refreshed ANALYTICS.CURATED_TRIPS successfully"
$$;

create or replace task daily_refresh_task
    WAREHOUSE = dev_wh
    SCHEDULE = 'USING CRON 0 2 * * * Europe/Amsterdam'
as 
    call refresh_curated_trips();

-- To test manually (without waiting for the schedule):
-- CALL refresh_curated_trips();

-- To actually activate the schedule (not done in this project):
-- ALTER TASK daily_refresh_task RESUME;