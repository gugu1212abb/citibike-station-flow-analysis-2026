CREATE OR REPLACE TABLE demand_day_type AS
WITH day_counts AS (
    SELECT
        CASE WHEN dayofweek(started_at) IN (0, 6)
             THEN 'weekend' ELSE 'weekday' END AS day_type,
        count(DISTINCT cast(started_at AS DATE)) AS days
    FROM rides_clean
    GROUP BY 1
),
hour_counts AS (
    SELECT
        CASE WHEN dayofweek(started_at) IN (0, 6)
             THEN 'weekend' ELSE 'weekday' END AS day_type,
        hour(started_at) AS hour_of_day,
        count(*) AS departures
    FROM rides_clean
    GROUP BY 1, 2
)
SELECT
    h.day_type,
    h.hour_of_day,
    d.days,
    h.departures,
    round(h.departures * 1.0 / d.days, 1) AS avg_departures_per_day
FROM hour_counts h
JOIN day_counts d USING (day_type);