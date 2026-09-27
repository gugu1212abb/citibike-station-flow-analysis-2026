CREATE OR REPLACE TABLE hourly_demand AS
WITH events AS (
    SELECT hour(started_at) AS hour_of_day, 'departure' AS event_type
    FROM rides_clean

    UNION ALL

    SELECT hour(ended_at) AS hour_of_day, 'arrival' AS event_type
    FROM rides_clean
)
SELECT
    hour_of_day,
    count(*) FILTER (WHERE event_type = 'departure') AS departures,
    count(*) FILTER (WHERE event_type = 'arrival') AS arrivals,
    count(*) FILTER (WHERE event_type = 'departure')
      - count(*) FILTER (WHERE event_type = 'arrival') AS net_outflow
FROM events
GROUP BY hour_of_day;