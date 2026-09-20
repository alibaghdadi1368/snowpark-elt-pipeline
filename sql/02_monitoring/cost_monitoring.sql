-- ============================================================
-- Cost Monitoring Queries
-- ============================================================

SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
ORDER BY START_TIME DESC
LIMIT 10;

SELECT SUM(CREDITS_USED) AS total_credit_usage
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE WAREHOUSE_NAME = 'DEV_WH';

SHOW WAREHOUSES;

SHOW TASKS LIKE 'daily_refresh_task';