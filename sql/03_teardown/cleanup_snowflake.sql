-- ============================================================
-- Teardown / Cleanup — Snowpark project
-- ============================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE dev_wh;

ALTER TASK IF EXISTS portfolio_db.analytics.daily_refresh_task SUSPEND;
ALTER WAREHOUSE dev_wh SUSPEND;

SHOW WAREHOUSES;

-- Objects created specifically by this project (uncomment to drop):
-- DROP TABLE IF EXISTS portfolio_db.analytics.curated_trips;
-- DROP TABLE IF EXISTS portfolio_db.analytics.trip_category_summary;
-- DROP PROCEDURE IF EXISTS portfolio_db.analytics.refresh_curated_trips();
-- DROP TASK IF EXISTS portfolio_db.analytics.daily_refresh_task;
-- DROP FUNCTION IF EXISTS portfolio_db.analytics.classify_trip_quality_udf(FLOAT);