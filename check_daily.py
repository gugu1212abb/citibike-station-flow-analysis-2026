import duckdb

con = duckdb.connect("citibike.duckdb", read_only=True)

rows = con.execute("""
WITH events AS (
    SELECT
        start_station_id AS station_id,
        started_at AS event_time,
        1 AS net_change
    FROM rides_clean

    UNION ALL

    SELECT
        end_station_id AS station_id,
        ended_at AS event_time,
        -1 AS net_change
    FROM rides_clean
),
daily AS (
    SELECT
        cast(event_time AS DATE) AS ride_date,
        hour(event_time) AS hour_of_day,
        sum(net_change) AS net_outflow
    FROM events
    WHERE station_id = '5659.05'
      AND event_time >= TIMESTAMP '2026-04-01'
      AND event_time < TIMESTAMP '2026-05-01'
      AND dayofweek(event_time) NOT IN (0, 6)
      AND hour(event_time) IN (8, 17, 18)
    GROUP BY 1, 2
)
SELECT
    hour_of_day,
    count(*) AS days_with_rides,
    round(avg(net_outflow), 1) AS avg_daily_net,
    median(net_outflow) AS median_daily_net,
    count(*) FILTER (WHERE net_outflow > 0) AS net_outflow_days,
    count(*) FILTER (WHERE net_outflow < 0) AS net_inflow_days
FROM daily
GROUP BY hour_of_day
ORDER BY hour_of_day
""").fetchall()

for row in rows:
    print(row)

con.close()