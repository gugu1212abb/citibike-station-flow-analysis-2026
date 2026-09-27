import duckdb

con = duckdb.connect("citibike.duckdb", read_only=True)

result = con.execute("""
WITH typed AS (
    SELECT
        ride_id,
        nullif(trim(start_station_id), '') AS start_id,
        nullif(trim(end_station_id), '') AS end_id,
        try_cast(started_at AS TIMESTAMP) AS start_time,
        try_cast(ended_at AS TIMESTAMP) AS end_time
    FROM rides_raw
)
SELECT
    count(*) AS total_rows,
    count(*) FILTER (WHERE ride_id IS NULL OR trim(ride_id) = '')
        AS missing_ride_id,
    count(*) FILTER (WHERE start_id IS NULL) AS missing_start_station,
    count(*) FILTER (WHERE end_id IS NULL) AS missing_end_station,
    count(*) FILTER (WHERE start_time IS NULL OR end_time IS NULL)
        AS invalid_time,
    count(*) FILTER (WHERE end_time <= start_time)
        AS non_positive_duration,
    count(*) FILTER (WHERE end_time > start_time + INTERVAL '24 hours')
        AS over_24_hours
FROM typed
""")

columns = [column[0] for column in result.description]
values = result.fetchone()

for name, value in zip(columns, values):
    print(f"{name}: {value:,}")

con.close()