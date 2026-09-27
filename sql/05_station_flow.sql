CREATE OR REPLACE TABLE station_hour_flow AS
WITH events AS (
    SELECT
        start_station_id AS station_id,
        start_station_name AS station_name,
        started_at AS event_time,
        1 AS departure,
        0 AS arrival
    FROM rides_clean

    UNION ALL

    SELECT
        end_station_id AS station_id,
        end_station_name AS station_name,
        ended_at AS event_time,
        0 AS departure,
        1 AS arrival
    FROM rides_clean
),
counts AS (
    SELECT
        station_id,
        max(station_name) AS station_name,
        CASE WHEN dayofweek(event_time) IN (0, 6)
             THEN 'weekend' ELSE 'weekday' END AS day_type,
        hour(event_time) AS hour_of_day,
        sum(departure) AS departures,
        sum(arrival) AS arrivals
    FROM events
    WHERE event_time >= TIMESTAMP '2026-04-01'
      AND event_time < TIMESTAMP '2026-05-01'
    GROUP BY station_id, day_type, hour_of_day
)
SELECT
    *,
    CASE WHEN day_type = 'weekday' THEN 22 ELSE 8 END AS days,
    round(
        (departures - arrivals) * 1.0
        / CASE WHEN day_type = 'weekday' THEN 22 ELSE 8 END, 1
    ) AS avg_net_outflow_per_day
FROM counts;